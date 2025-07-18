#!/usr/bin/env python3
"""
Demo script showing how to use Pyrogram session strings
This script demonstrates basic usage of generated session strings
"""

import asyncio
import os
from pyrogram import Client
from pyrogram.errors import AuthKeyUnregistered, FloodWait
from utils import print_success, print_error, print_info, print_warning

class SessionStringDemo:
    """Demo class for using session strings"""
    
    def __init__(self, session_string):
        self.session_string = session_string
        self.client = None
    
    async def connect(self):
        """Connect to Telegram using session string"""
        try:
            self.client = Client(
                name="demo_session",
                session_string=self.session_string,
                in_memory=True
            )
            
            print_info("Connecting to Telegram...")
            await self.client.start()
            
            # Get account info
            me = await self.client.get_me()
            if me.is_bot:
                print_success(f"Connected as Bot: {me.first_name} (@{me.username})")
            else:
                account_info = f"{me.first_name}"
                if me.last_name:
                    account_info += f" {me.last_name}"
                if me.username:
                    account_info += f" (@{me.username})"
                print_success(f"Connected as User: {account_info}")
            
            return True
            
        except AuthKeyUnregistered:
            print_error("Session string is invalid or expired!")
            return False
        except Exception as e:
            print_error(f"Connection failed: {str(e)}")
            return False
    
    async def demo_basic_operations(self):
        """Demonstrate basic operations"""
        if not self.client:
            print_error("Not connected to Telegram!")
            return
        
        try:
            print_info("Running basic operations demo...")
            
            # Send message to saved messages
            await self.client.send_message(
                "me", 
                "🚀 **Demo Message**\n\n"
                "This message was sent using a Pyrogram session string!\n"
                f"Timestamp: {self.get_current_time()}"
            )
            print_success("Message sent to Saved Messages!")
            
            # Get recent messages from saved messages
            print_info("Fetching recent messages...")
            messages = []
            async for message in self.client.get_chat_history("me", limit=3):
                if message.text:
                    messages.append(message.text[:50] + "..." if len(message.text) > 50 else message.text)
            
            if messages:
                print_success(f"Found {len(messages)} recent messages")
                for i, msg in enumerate(messages, 1):
                    print(f"  {i}. {msg}")
            
            # Get dialogs count
            dialog_count = 0
            async for dialog in self.client.get_dialogs(limit=100):
                dialog_count += 1
            
            print_success(f"Total dialogs: {dialog_count}")
            
        except FloodWait as e:
            print_warning(f"Rate limited! Wait {e.value} seconds")
        except Exception as e:
            print_error(f"Operation failed: {str(e)}")
    
    async def demo_advanced_operations(self):
        """Demonstrate advanced operations"""
        if not self.client:
            print_error("Not connected to Telegram!")
            return
        
        try:
            print_info("Running advanced operations demo...")
            
            # Get account details
            me = await self.client.get_me()
            
            details = f"""
📊 **Account Details:**
🆔 ID: {me.id}
👤 Name: {me.first_name} {me.last_name or ''}
📱 Username: @{me.username if me.username else 'No username'}
📞 Phone: {me.phone_number if me.phone_number else 'Hidden'}
🤖 Is Bot: {'Yes' if me.is_bot else 'No'}
✅ Verified: {'Yes' if me.is_verified else 'No'}
⭐ Premium: {'Yes' if me.is_premium else 'No'}
"""
            
            print_success("Account details retrieved:")
            print(details)
            
            # Test file operations (send and receive)
            print_info("Testing file operations...")
            
            # Create a test file
            test_content = f"""
🔧 **Pyrogram Session String Test**

This file was created and sent using a session string.

Session Details:
- Generated: {self.get_current_time()}
- Client: Pyrogram v2.0+
- Status: Working properly

⚠️ Security reminder: Keep your session strings private!
"""
            
            with open("test_file.txt", "w") as f:
                f.write(test_content)
            
            # Send file to saved messages
            await self.client.send_document("me", "test_file.txt", caption="📄 Test file from session string")
            print_success("Test file sent successfully!")
            
            # Clean up
            os.remove("test_file.txt")
            
        except Exception as e:
            print_error(f"Advanced operations failed: {str(e)}")
    
    async def disconnect(self):
        """Disconnect from Telegram"""
        if self.client:
            await self.client.stop()
            print_info("Disconnected from Telegram")
    
    def get_current_time(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def main():
    """Main demo function"""
    print("="*60)
    print("🚀 PYROGRAM SESSION STRING DEMO")
    print("="*60)
    
    # Get session string from user
    session_string = input("Enter your session string: ").strip()
    
    if not session_string:
        print_error("Session string is required!")
        return
    
    # Create demo instance
    demo = SessionStringDemo(session_string)
    
    try:
        # Connect to Telegram
        if await demo.connect():
            print_info("Running demonstration...")
            
            # Run basic operations
            await demo.demo_basic_operations()
            
            # Ask if user wants to see advanced operations
            print()
            choice = input("Run advanced operations demo? (y/n): ").lower()
            if choice == 'y':
                await demo.demo_advanced_operations()
            
            print_success("Demo completed successfully!")
        
    except KeyboardInterrupt:
        print_warning("Demo interrupted by user")
    except Exception as e:
        print_error(f"Demo failed: {str(e)}")
    finally:
        await demo.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_warning("Demo terminated by user")