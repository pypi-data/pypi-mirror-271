#!/usr/bin/env python3
"""Rumble Chat Actor

Automatically interact with your Rumble livestream chats.
S.D.G."""

import textwrap
import time
from cocorum import RumbleAPI, utils
from cocorum.ssechat import SSEChat
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#How long to wait after performing any browser action, for the webpage to load its response
BROWSER_ACTION_DELAY = 2

#Popout chat url. Format with stream_id_b10
CHAT_URL = "https://rumble.com/chat/popup/{stream_id_b10}"

#Maximum chat message length
MAX_MESSAGE_LEN = 200

#Message split across multiple lines must not be longer than this
MAX_MULTIMESSAGE_LEN = 1000

#Prefix to all actor messages
BOT_MESSAGE_PREFIX = "🤖: "

#How commands always start
COMMAND_PREFIX = "!"

#Levels of mute to discipline a user with
MUTE_LEVELS = {
    "5" : "cmi js-btn-mute-current-5",
    "stream" : "cmi js-btn-mute-current",
    "forever" : "cmi js-btn-mute-for-account",
    }

class ChatCommand():
    """A chat command, internal use only"""
    def __init__(self, name, actor, cooldown = BROWSER_ACTION_DELAY, amount_cents = 0, whitelist_badges = ["moderator"], target = None):
        """name: The !name of the command
    actor: The RumleChatActor host object
    amount_cents: The minimum cost of the command. Defaults to free
    whitelist_badges: Badges which if borne give the user free-of-charge command access
    target: The function(message, actor) to call on successful command usage. Defaults to self.run"""
        assert " " not in name, "Name cannot contain spaces"
        self.name = name
        self.actor = actor
        assert cooldown >= BROWSER_ACTION_DELAY, f"Cannot set a cooldown shorter than {BROWSER_ACTION_DELAY}"
        self.cooldown = cooldown
        self.amount_cents = amount_cents #Cost of the command
        self.whitelist_badges = ["admin"] + whitelist_badges #Admin always has free-of-charge usage
        self.last_use_time = 0 #Last time the command was called
        self.target = target

    def call(self, message):
        """The command was called"""

        #The command is still on cooldown
        if (curtime := time.time()) - self.last_use_time < self.cooldown:
            self.actor.send_message(f"@{message.user.username} That command is still on cooldown. Try again in {int(self.last_use_time + self.cooldown - curtime + 0.5)} seconds.")

            return

        #the user did not pay enough for the command and they do not have a free pass
        if message.rant_price_cents < self.amount_cents and not (True in [badge.slug in self.whitelist_badges for badge in message.user.badges]):
            self.actor.send_message(f"@{message.user.username} That command costs ${self.amount_cents/100:.2f}.")
            return

        #the command was called successfully
        self.run(message)

        #Mark the last use time for cooldown
        self.last_use_time = time.time()

    def run(self, message):
        """Dummy run method"""
        if self.target:
            self.target(message, self.actor)
            return

        #Run method was never defined
        self.actor.send_message(f"@{message.user.username} Hello, this command never had a target defined. :-)")

class ExclusiveChatCommand(ChatCommand):
    """Chat command that only certain badges can use"""
    def __init__(self, name, actor, cooldown = BROWSER_ACTION_DELAY, amount_cents = 0, allowed_badges = ["subscriber"], whitelist_badges = ["moderator"], target = None):
        """name: The !name of the command
    actor: The RumleChatActor host object
    amount_cents: The minimum cost of the command. Defaults to free
    allowed_badges: Badges which must be borne to use the command at all
    whitelist_badges: Badges which if borne give the user free-of-charge command access
    target: The function(message, actor) to call on successful command usage. Defaults to self.run"""
        super().__init__(name, actor, cooldown = BROWSER_ACTION_DELAY, amount_cents = 0, whitelist_badges = ["moderator"], target = target)
        #Admin can always call any command
        self.allowed_badges = ["admin"] + allowed_badges

    def call(self, message):
        """The command was called"""
        #the user does not have the required badge
        if not (True in [badge.slug in self.allowed_badges for badge in message.user.badges]):
            self.actor.send_message(f"@{message.user.username} That command is exclusive to: " + ", ".join(self.allowed_badges))
            return

        #Proceed with normal command processing
        super().call(message)

class RumbleChatActor():
    """Actor that interacts with Rumble chat"""
    def __init__(self, stream_id = None, init_message = "Hello, Rumble world!", profile_dir = None, credentials = None, api_url = None):
        """stream_id: The stream ID you want to connect to. Defaults to latest livestream
    init_message: What to say when the actor starts up.
    profile_dir: The Firefox profile directory to use. Defaults to temp (sign-in not saved)
    credentials: The (username, password) to log in with. Defaults to manual log in"""

        #Get Live Stream API
        if api_url:
            self.rum_api = RumbleAPI(api_url)
        else:
            self.rum_api = None

        #A stream ID was passed
        if stream_id:
            self.stream_id, self.stream_id_b10 = utils.stream_id_36_and_10(stream_id)

            #It is not our livestream or we have no Live Stream API, LS API functions are not available
            if not self.rum_api or self.stream_id not in self.rum_api.livestreams:
                self.api_stream = None

            #It is our livestream, we can use the Live Stream API
            else:
                self.api_stream = self.rum_api.livestreams[stream_id]

        #A stream ID was not passed
        else:
            assert self.rum_api, "Cannot auto-find stream ID without a Live Stream API url"
            self.api_stream = self.rum_api.latest_livestream

            #At least one live stream must be shown on the API
            assert self.api_stream, "No stream ID was passed and you are not live"

            self.stream_id = self.api_stream.stream_id
            self.stream_id_b10 = utils.stream_id_36_to_10(self.stream_id)

        #Get SSE chat and empty the mailbox
        self.ssechat = SSEChat(stream_id = self.stream_id)
        self.ssechat.clear_mailbox()

        #Set browser profile directory of we have one
        options = webdriver.FirefoxOptions()
        if profile_dir:
            options.add_argument("-profile")
            options.add_argument(profile_dir)

        #Get browser
        self.browser = webdriver.Firefox(options = options)
        self.browser.minimize_window()
        self.browser.get(CHAT_URL.format(stream_id_b10 = self.ssechat.stream_id_b10))
        assert "Chat" in self.browser.title

        #Sign in to chat, unless we are already. While there is a sign-in button...
        while sign_in_buttn := self.get_sign_in_button():
            #We have credentials
            if credentials:
                sign_in_buttn.click()
                time.sleep(BROWSER_ACTION_DELAY)
                self.browser.find_element(By.ID, "login-username").send_keys(credentials[0] + Keys.RETURN)
                self.browser.find_element(By.ID, "login-password").send_keys(credentials[1] + Keys.RETURN)
                break #We only need to do that once

            #We do not have credentials, ask for manual sign in
            self.browser.maximize_window()
            input("Please log in at the browser, then press enter here.")

            #Wait for signed in loading to complete
            time.sleep(BROWSER_ACTION_DELAY)

        #Find our username
        if credentials:
            self.username = credentials[0]
        elif self.rum_api:
            self.username = self.rum_api.username
        else:
            self.username = None
            while not self.username:
                self.username = input("Enter the username the actor is using: ")

        #Wait for potential further page load?
        time.sleep(BROWSER_ACTION_DELAY)

        #History of the bot's messages so they do not get loop processed
        self.sent_messages = []

        #Send an initialization message to get wether we are moderator or not
        self.send_message(init_message)

        #Wait until we get that message
        while (m := self.ssechat.get_message()).user.username != self.username:
            pass

        assert "moderator" in m.user.badges or "admin" in m.user.badges, "Actor cannot function without being a moderator"

        #Functions that are to be called on each message, must return False if the message was deleted
        self.message_actions = []

        #Instances of RumbleChatCommand, by name
        self.chat_commands = {}

        #Loop condition of the mainloop() method
        self.keep_running = True

    def get_sign_in_button(self):
        """Look for the sign in button"""
        try:
            return self.browser.find_element(By.CLASS_NAME, "chat--sign-in")
        except selenium.common.exceptions.NoSuchElementException:
            print("Could not find sign-in button, already signed in.")
            return None

    def send_message(self, text):
        """Send a message in chat (splits across lines if necessary)"""
        text = BOT_MESSAGE_PREFIX + text
        assert "\n" not in text, "Message cannot contain newlines"
        assert len(text) < MAX_MULTIMESSAGE_LEN, "Message is too long"
        for subtext in textwrap.wrap(text, width = MAX_MESSAGE_LEN):
            self.__send_message(subtext)

    def __send_message(self, text):
        """Send a message in chat"""
        assert len(text) < MAX_MESSAGE_LEN, f"Message with prefix cannot be longer than {MAX_MESSAGE_LEN} characters"
        self.sent_messages.append(text)
        self.browser.find_element(By.ID, "chat-message-text-input").send_keys(text + Keys.RETURN)
        time.sleep(BROWSER_ACTION_DELAY)

    def hover_element(self, element):
        """Hover over a selenium element"""
        ActionChains(self.browser).move_to_element(element).perform()

    def open_moderation_menu(self, message):
        """Open the moderation menu of a message"""

        #The passed message was a li element
        if isinstance(message, webdriver.remote.webelement.WebElement) and message.tag_name == "li":
            message_li = message
            message_id = message_li.get_attribute("data-message-id")

        #Find the message by ID
        elif isinstance(message, int):
            message_id = message
            message_li = self.browser.find_element(By.XPATH, f"//li[@class='chat-history--row js-chat-history-item'][@data-message-id='{message_id}']")

        #The message has a message ID attribute
        elif hasattr(message, "message_id"):
            message_id = message.message_id
            message_li = self.browser.find_element(By.XPATH, f"//li[@class='chat-history--row js-chat-history-item'][@data-message-id='{message_id}']")

        #Not a valid message type
        else:
            raise TypeError("Message must be ID, li element, or have message_id attribute")

        #Hover over the message
        self.hover_element(message_li)
        #Find the moderation menu
        menu_bttn = self.browser.find_element(By.XPATH, f"//li[@class='chat-history--row js-chat-history-item'][@data-message-id='{message_id}']/button[@class='js-moderate-btn chat-history--kebab-button']")
        #Click the moderation menu button
        menu_bttn.click()

        return message_id

    def delete_message(self, message):
        """Delete a message in the chat"""
        m_id = self.open_moderation_menu(message)
        del_bttn = self.browser.find_element(By.XPATH, f"//button[@class='cmi js-btn-delete-current'][@data-message-id='{m_id}']")
        del_bttn.click()
        time.sleep(BROWSER_ACTION_DELAY)

        #Confirm the confirmation dialog
        Alert(self.browser).accept()

    def mute_by_message(self, message, mute_level = "5"):
        """Mute a user by message"""
        self.open_moderation_menu(message)
        timeout_bttn = self.browser.find_element(By.XPATH, f"//button[@class='{MUTE_LEVELS[mute_level]}']")
        timeout_bttn.click()

    def mute_by_appearname(self, name, mute_level = "5"):
        """Mute a user by the name they are appearing with"""
        #Find any chat message by this user
        message_li = self.browser.find_element(By.XPATH, f"//li[@class='chat-history--row js-chat-history-item'][@data-username='{name}']")
        self.mute_by_message(message = message_li, mute_level = mute_level)

    def pin_message(self, message):
        """Pin a message by ID or li element"""
        self.open_moderation_menu(message)
        pin_bttn = self.browser.find_element(By.XPATH, "//button[@class='cmi js-btn-pin-current']")
        pin_bttn.click()

    def unpin_message(self):
        """Unpin the currently pinned message"""
        try:
            unpin_bttn = self.browser.find_element(By.XPATH, "//button[@data-js='remove_pinned_message_button']")
        except selenium.common.exceptions.NoSuchElementException:
            return False #No message was pinned

        unpin_bttn.click()
        return True

    def quit(self):
        """Shut down everything"""
        self.browser.quit()
        # TODO how to close an SSEClient?
        # self.ssechat.client.close()

    def __run_if_command(self, message):
        """Check if a message is a command, and run it if so"""
        #Not a command
        if not message.text.startswith(COMMAND_PREFIX):
            return

        #Get command name
        name = message.text.split()[0].removeprefix(COMMAND_PREFIX)

        #Is not a valid command
        if name not in self.chat_commands:
            self.send_message(f"@{message.user.username} That is not a registered command.")
            return

        self.chat_commands[name].call(message)

    def register_command(self, command, name = None):
        """Register a command"""
        #Is a ChatCommand instance
        if isinstance(command, ChatCommand):
            assert not name or name == command.name, "ChatCommand instance has different name than one passed"
            self.chat_commands[command.name] = command

        #Is a callable
        elif callable(command):
            assert name, "Name cannot be None if command is a callable"
            assert " " not in name, "Name cannot contain spaces"
            self.chat_commands[name] = ChatCommand(name = name, actor = self, target = command)

    def register_message_action(self, action):
        """Register an action callable to be run on every message
    - Action will be passed cocorum.ssechat.SSEChatMessage() and this actor
    - Action should return True if the message survived the action
    - Action should return False if the message was deleted by the action"""
        assert callable(action), "Action must be a callable"
        self.message_actions.append(action)

    def __process_message(self, message):
        """Process a single SSE Chat message"""
        #Do not do anything with the message if it matches one we sent before
        if message.text in self.sent_messages:
            return

        for action in self.message_actions:
            if message.message_id in self.ssechat.deleted_message_ids or not action(message, self): #The message got deleted, possibly by this action
                return

        self.__run_if_command(message)

    def mainloop(self):
        """Run the actor forever"""
        while self.keep_running:
            m = self.ssechat.get_message()
            if not m: #Chat has closed
                self.keep_running = False
                return
            self.__process_message(m)
