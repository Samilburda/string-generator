"""
Session Manager - Handles session string generation and management
"""

import os
import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AuthKeyUnregistered
from pyrogram.errors import PhoneNumberInvalid, PhoneCodeInvalid, SessionPasswordNeeded
from pyrogram.errors import FloodWait, BadRequest
from utils import print_error, print_success, print_info, print_warning
from config import Config

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class SessionManager:
    """Manages Pyrogram session string generation and operations"""
    
    def __init__(self, api_id=None, api_hash=None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.config = Config()
    
    async def generate_user_session(self, phone_number=None):
        """
        Generate session string for user account
        
        Args:
            phone_number (str, optional): Phone number for faster login
            
        Returns:
            str: Session string if successful, None otherwise
        """
        try:
            # Create client with in-memory session
            client = Client(
                name="temp_session",
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=phone_number,
                in_memory=True
            )
            
            print_info("Connecting to Telegram...")
            await client.start()
            
            # Export session string
            session_string = await client.export_session_string()
            
            # Get user info
            me = await client.get_me()
            user_info = f"{me.first_name}"
            if me.last_name:
                user_info += f" {me.last_name}"
            if me.username:
                user_info += f" (@{me.username})"
            
            print_success(f"Successfully logged in as: {user_info}")
            
            await client.stop()
            return session_string
            
        except ApiIdInvalid:
            print_error("Invalid API ID! Please check your credentials.")
            return None
        except ApiIdPublishedFlood:
            print_error("API ID has been published and is now limited. Please use a different API ID.")
            return None
        except PhoneNumberInvalid:
            print_error("Invalid phone number format!")
            return None
        except SessionPasswordNeeded:
            print_error("Two-factor authentication is enabled. Please disable it temporarily or use a different method.")
            return None
        except FloodWait as e:
            print_error(f"Rate limited! Please wait {e.value} seconds before trying again.")
            return None
        except Exception as e:
            print_error(f"Error generating user session: {str(e)}")
            return None
    
    async def generate_bot_session(self, bot_token):
        """
        Generate session string for bot account
        
        Args:
            bot_token (str): Bot token from BotFather
            
        Returns:
            str: Session string if successful, None otherwise
        """
        try:
            # Create bot client with in-memory session
            client = Client(
                name="temp_bot_session",
                bot_token=bot_token,
                in_memory=True
            )
            
            print_info("Connecting to Telegram as bot...")
            await client.start()
            
            # Export session string
            session_string = await client.export_session_string()
            
            # Get bot info
            me = await client.get_me()
            bot_info = f"{me.first_name}"
            if me.username:
                bot_info += f" (@{me.username})"
            
            print_success(f"Successfully connected as bot: {bot_info}")
            
            await client.stop()
            return session_string
            
        except AuthKeyUnregistered:
            print_error("Invalid bot token! Please check your token from BotFather.")
            return None
        except FloodWait as e:
            print_error(f"Rate limited! Please wait {e.value} seconds before trying again.")
            return None
        except Exception as e:
            print_error(f"Error generating bot session: {str(e)}")
            return None
    
    async def convert_session_file(self, session_name):
        """
        Convert existing session file to session string
        
        Args:
            session_name (str): Name of the session file (without .session extension)
            
        Returns:
            str: Session string if successful, None otherwise
        """
        try:
            session_file = f"{session_name}.session"
            if not os.path.exists(session_file):
                print_error(f"Session file '{session_file}' not found!")
                return None
            
            # Create client with existing session file
            client = Client(session_name)
            
            print_info("Loading existing session...")
            await client.start()
            
            # Export session string
            session_string = await client.export_session_string()
            
            # Get account info
            me = await client.get_me()
            if me.is_bot:
                account_info = f"Bot: {me.first_name}"
                if me.username:
                    account_info += f" (@{me.username})"
            else:
                account_info = f"User: {me.first_name}"
                if me.last_name:
                    account_info += f" {me.last_name}"
                if me.username:
                    account_info += f" (@{me.username})"
            
            print_success(f"Successfully loaded session for: {account_info}")
            
            await client.stop()
            return session_string
            
        except Exception as e:
            print_error(f"Error converting session file: {str(e)}")
            return None
    
    async def send_to_saved_messages(self, session_string):
        """
        Send session string to user's saved messages
        
        Args:
            session_string (str): The session string to send
        """
        try:
            # Create temporary client to send message
            client = Client(
                name="temp_sender",
                api_id=self.api_id,
                api_hash=self.api_hash,
                session_string=session_string
            )
            
            await client.start()
            
            message = (
                "🔑 **Pyrogram Session String**\n\n"
                f"`{session_string}`\n\n"
                "⚠️ **Security Warning:**\n"
                "• Keep this string private and secure\n"
                "• Do not share it with anyone\n"
                "• It provides full access to your account\n"
                "• Store it in a safe location\n\n"
                f"Generated on: {self.config.get_current_timestamp()}"
            )
            
            await client.send_message("me", message)
            print_success("Session string sent to your Saved Messages!")
            
            await client.stop()
            
        except Exception as e:
            print_warning(f"Could not send to saved messages: {str(e)}")
    
    async def test_session_string(self, session_string):
        """
        Test if a session string is working
        
        Args:
            session_string (str): Session string to test
            
        Returns:
            tuple: (is_valid, account_info)
        """
        try:
            client = Client(
                name="test_session",
                session_string=session_string,
                in_memory=True
            )
            
            await client.start()
            
            # Get account info
            me = await client.get_me()
            if me.is_bot:
                account_info = f"Bot: {me.first_name}"
                if me.username:
                    account_info += f" (@{me.username})"
            else:
                account_info = f"User: {me.first_name}"
                if me.last_name:
                    account_info += f" {me.last_name}"
                if me.username:
                    account_info += f" (@{me.username})"
            
            await client.stop()
            return True, account_info
            
        except Exception as e:
            logger.error(f"Session test failed: {str(e)}")
            return False, None
