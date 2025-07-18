"""
Session Validator - Validates and tests session strings
"""

import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, AuthKeyUnregistered
from pyrogram.errors import FloodWait, BadRequest
from utils import print_error, print_success, print_info, print_warning

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class SessionValidator:
    """Validates Pyrogram session strings"""
    
    def __init__(self):
        pass
    
    async def validate_session_string(self, session_string):
        """
        Validate a session string by attempting to connect
        
        Args:
            session_string (str): Session string to validate
            
        Returns:
            tuple: (is_valid, account_info)
        """
        try:
            # Basic format validation
            if not self._is_valid_format(session_string):
                print_error("Invalid session string format!")
                return False, None
            
            # Create client with session string
            client = Client(
                name="validator_session",
                session_string=session_string,
                in_memory=True
            )
            
            print_info("Testing session string...")
            await client.start()
            
            # Get account information
            me = await client.get_me()
            account_info = self._format_account_info(me)
            
            # Test basic functionality
            await self._test_basic_functionality(client)
            
            await client.stop()
            return True, account_info
            
        except AuthKeyUnregistered:
            print_error("Session string is invalid or expired!")
            return False, None
        except SessionPasswordNeeded:
            print_error("Two-factor authentication is enabled. Session may be valid but requires 2FA.")
            return False, None
        except FloodWait as e:
            print_error(f"Rate limited! Please wait {e.value} seconds before trying again.")
            return False, None
        except Exception as e:
            print_error(f"Validation failed: {str(e)}")
            return False, None
    
    def _is_valid_format(self, session_string):
        """
        Check if session string has valid format
        
        Args:
            session_string (str): Session string to check
            
        Returns:
            bool: True if format is valid
        """
        try:
            # Basic checks
            if not session_string or not isinstance(session_string, str):
                return False
            
            # Remove whitespace
            session_string = session_string.strip()
            
            # Check minimum length (Pyrogram session strings are typically quite long)
            if len(session_string) < 100:
                return False
            
            # Check for valid base64-like characters
            import string
            valid_chars = string.ascii_letters + string.digits + '+/='
            if not all(c in valid_chars for c in session_string):
                return False
            
            return True
            
        except Exception:
            return False
    
    def _format_account_info(self, user):
        """
        Format user account information
        
        Args:
            user: Pyrogram User object
            
        Returns:
            str: Formatted account information
        """
        if user.is_bot:
            info = f"🤖 Bot: {user.first_name}"
            if user.username:
                info += f" (@{user.username})"
        else:
            info = f"👤 User: {user.first_name}"
            if user.last_name:
                info += f" {user.last_name}"
            if user.username:
                info += f" (@{user.username})"
            
            # Add additional user info
            if user.phone_number:
                info += f"\n📱 Phone: {user.phone_number}"
            if user.is_verified:
                info += "\n✅ Verified Account"
            if user.is_premium:
                info += "\n⭐ Premium Account"
        
        return info
    
    async def _test_basic_functionality(self, client):
        """
        Test basic functionality of the session
        
        Args:
            client: Pyrogram Client instance
        """
        try:
            # Test getting dialogs (basic functionality)
            dialogs = []
            async for dialog in client.get_dialogs(limit=1):
                dialogs.append(dialog)
            
            print_info(f"✅ Basic functionality test passed")
            
        except Exception as e:
            print_warning(f"Basic functionality test failed: {str(e)}")
    
    async def validate_multiple_sessions(self, session_strings):
        """
        Validate multiple session strings
        
        Args:
            session_strings (list): List of session strings to validate
            
        Returns:
            dict: Results for each session string
        """
        results = {}
        
        for i, session_string in enumerate(session_strings):
            print_info(f"Validating session {i+1}/{len(session_strings)}...")
            
            is_valid, account_info = await self.validate_session_string(session_string)
            results[i] = {
                'session_string': session_string,
                'is_valid': is_valid,
                'account_info': account_info
            }
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(1)
        
        return results
    
    async def check_session_permissions(self, session_string):
        """
        Check what permissions the session has
        
        Args:
            session_string (str): Session string to check
            
        Returns:
            dict: Available permissions and capabilities
        """
        try:
            client = Client(
                name="permission_checker",
                session_string=session_string,
                in_memory=True
            )
            
            await client.start()
            
            permissions = {
                'can_send_messages': False,
                'can_read_messages': False,
                'can_manage_chat': False,
                'is_bot': False,
                'can_access_saved_messages': False
            }
            
            # Check if it's a bot
            me = await client.get_me()
            permissions['is_bot'] = me.is_bot
            
            # Test reading messages (saved messages)
            try:
                async for message in client.get_chat_history("me", limit=1):
                    permissions['can_read_messages'] = True
                    permissions['can_access_saved_messages'] = True
                    break
            except Exception:
                pass
            
            # Test sending messages (to saved messages)
            try:
                test_message = await client.send_message("me", "🧪 Permission test message")
                permissions['can_send_messages'] = True
                # Clean up test message
                await client.delete_messages("me", test_message.id)
            except Exception:
                pass
            
            await client.stop()
            return permissions
            
        except Exception as e:
            print_error(f"Permission check failed: {str(e)}")
            return None
