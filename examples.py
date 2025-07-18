"""
Usage examples for Pyrogram session strings
"""

from utils import print_banner, print_success, print_info, print_highlight, print_warning

class SessionExamples:
    """Display usage examples for session strings"""
    
    def __init__(self):
        pass
    
    def display_all_examples(self):
        """Display all usage examples"""
        print_banner("PYROGRAM SESSION STRING USAGE EXAMPLES")
        
        self.basic_usage_example()
        self.bot_usage_example()
        self.advanced_usage_example()
        self.error_handling_example()
        self.best_practices_example()
    
    def basic_usage_example(self):
        """Display basic usage example"""
        print_highlight("1. BASIC USER SESSION USAGE")
        print_info("Here's how to use a user session string:")
        
        code = '''
from pyrogram import Client
import asyncio

async def main():
    # Your session string (replace with actual string)
    session_string = "your_session_string_here"
    
    # Create client with session string
    app = Client(
        name="my_app",
        session_string=session_string
    )
    
    async with app:
        # Get your account info
        me = await app.get_me()
        print(f"Logged in as: {me.first_name}")
        
        # Send message to saved messages
        await app.send_message("me", "Hello from session string!")
        
        # Get recent messages
        async for message in app.get_chat_history("me", limit=5):
            print(f"Message: {message.text}")

if __name__ == "__main__":
    asyncio.run(main())
'''
        print(code)
        print("-" * 60)
    
    def bot_usage_example(self):
        """Display bot usage example"""
        print_highlight("2. BOT SESSION USAGE")
        print_info("Here's how to use a bot session string:")
        
        code = '''
from pyrogram import Client
import asyncio

async def main():
    # Your bot session string
    bot_session_string = "your_bot_session_string_here"
    
    # Create bot client
    bot = Client(
        name="my_bot",
        session_string=bot_session_string
    )
    
    async with bot:
        # Get bot info
        me = await bot.get_me()
        print(f"Bot: {me.first_name} (@{me.username})")
        
        # Handle messages (example)
        @bot.on_message()
        async def handle_message(client, message):
            if message.text == "/start":
                await message.reply("Hello! I'm running with session string!")
        
        # Start bot
        print("Bot is running...")
        await bot.idle()

if __name__ == "__main__":
    asyncio.run(main())
'''
        print(code)
        print("-" * 60)
    
    def advanced_usage_example(self):
        """Display advanced usage example"""
        print_highlight("3. ADVANCED SESSION USAGE")
        print_info("Advanced features with session strings:")
        
        code = '''
from pyrogram import Client, filters
import asyncio
import os

class TelegramApp:
    def __init__(self, session_string):
        self.app = Client(
            name="advanced_app",
            session_string=session_string
        )
        
        # Register handlers
        self.app.on_message(filters.private & filters.text)(self.handle_private_message)
        self.app.on_message(filters.group & filters.command("stats"))(self.handle_stats)
    
    async def handle_private_message(self, client, message):
        """Handle private messages"""
        await message.reply(f"Hello {message.from_user.first_name}!")
    
    async def handle_stats(self, client, message):
        """Handle stats command in groups"""
        chat = await client.get_chat(message.chat.id)
        members_count = await client.get_chat_members_count(message.chat.id)
        
        stats = f"""
📊 **Chat Statistics**
👥 Members: {members_count}
💬 Chat: {chat.title}
🆔 ID: {chat.id}
        """
        await message.reply(stats)
    
    async def start(self):
        """Start the application"""
        await self.app.start()
        print("✅ Application started successfully!")
        
        # Get account info
        me = await self.app.get_me()
        print(f"👤 Logged in as: {me.first_name}")
        
        await self.app.idle()
    
    async def stop(self):
        """Stop the application"""
        await self.app.stop()
        print("🛑 Application stopped.")

async def main():
    # Get session string from environment variable
    session_string = os.getenv("PYROGRAM_SESSION_STRING")
    
    if not session_string:
        print("❌ Please set PYROGRAM_SESSION_STRING environment variable")
        return
    
    app = TelegramApp(session_string)
    
    try:
        await app.start()
    except KeyboardInterrupt:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
'''
        print(code)
        print("-" * 60)
    
    def error_handling_example(self):
        """Display error handling example"""
        print_highlight("4. ERROR HANDLING")
        print_info("Proper error handling with session strings:")
        
        code = '''
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, AuthKeyUnregistered
from pyrogram.errors import FloodWait, BadRequest
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def robust_session_usage(session_string):
    """Use session string with robust error handling"""
    
    try:
        # Create client
        app = Client(
            name="robust_app",
            session_string=session_string
        )
        
        # Start client
        await app.start()
        logger.info("✅ Successfully connected to Telegram")
        
        # Get account info
        me = await app.get_me()
        logger.info(f"👤 Logged in as: {me.first_name}")
        
        # Your app logic here
        await app.send_message("me", "✅ Session is working properly!")
        
        # Stop client
        await app.stop()
        
    except AuthKeyUnregistered:
        logger.error("❌ Session string is invalid or expired!")
        logger.error("💡 Please generate a new session string")
        
    except SessionPasswordNeeded:
        logger.error("❌ Two-factor authentication is enabled")
        logger.error("💡 Please disable 2FA temporarily or use a different method")
        
    except FloodWait as e:
        logger.error(f"❌ Rate limited! Wait {e.value} seconds")
        logger.error("💡 Please try again later")
        
    except BadRequest as e:
        logger.error(f"❌ Bad request: {e}")
        logger.error("💡 Check your session string and try again")
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        logger.error("💡 Please check your session string and network connection")

async def main():
    session_string = "your_session_string_here"
    await robust_session_usage(session_string)

if __name__ == "__main__":
    asyncio.run(main())
'''
        print(code)
        print("-" * 60)
    
    def best_practices_example(self):
        """Display best practices"""
        print_highlight("5. BEST PRACTICES")
        print_info("Best practices for session string usage:")
        
        practices = '''
🔐 SECURITY BEST PRACTICES:

1. Environment Variables:
   - Store session strings in environment variables
   - Never hardcode them in source code
   - Use .env files for local development

2. Session Management:
   - Use different sessions for different applications
   - Regularly rotate session strings
   - Monitor account activity

3. Error Handling:
   - Always handle AuthKeyUnregistered exceptions
   - Implement retry logic for FloodWait errors
   - Log errors for debugging

4. Application Structure:
   - Use classes for better organization
   - Implement proper startup/shutdown procedures
   - Use async context managers when possible

5. Production Deployment:
   - Use secure credential management systems
   - Implement proper logging
   - Set up monitoring and alerts
   - Use process managers (systemd, supervisor, etc.)

📝 EXAMPLE ENVIRONMENT SETUP:

# .env file
PYROGRAM_SESSION_STRING=your_session_string_here
LOG_LEVEL=INFO
CHAT_ID=123456789

# Python code
import os
from dotenv import load_dotenv

load_dotenv()

session_string = os.getenv("PYROGRAM_SESSION_STRING")
log_level = os.getenv("LOG_LEVEL", "INFO")
chat_id = int(os.getenv("CHAT_ID", "0"))

🚀 DEPLOYMENT TIPS:

1. Docker:
   - Use multi-stage builds
   - Set appropriate user permissions
   - Use secrets management

2. Cloud Platforms:
   - Use platform-specific secret managers
   - Configure proper environment variables
   - Set up health checks

3. Monitoring:
   - Log important events
   - Monitor memory and CPU usage
   - Set up alerting for errors
'''
        print(practices)
        print("-" * 60)
    
    def web_app_example(self):
        """Display web application example"""
        print_highlight("6. WEB APPLICATION INTEGRATION")
        print_info("Using session strings in web applications:")
        
        code = '''
from pyrogram import Client
from flask import Flask, request, jsonify
import asyncio
import os

app = Flask(__name__)

class TelegramService:
    def __init__(self, session_string):
        self.client = Client(
            name="web_app",
            session_string=session_string
        )
        self.is_connected = False
    
    async def connect(self):
        """Connect to Telegram"""
        if not self.is_connected:
            await self.client.start()
            self.is_connected = True
    
    async def disconnect(self):
        """Disconnect from Telegram"""
        if self.is_connected:
            await self.client.stop()
            self.is_connected = False
    
    async def send_message(self, chat_id, message):
        """Send message to chat"""
        await self.connect()
        result = await self.client.send_message(chat_id, message)
        return result.id
    
    async def get_chat_info(self, chat_id):
        """Get chat information"""
        await self.connect()
        chat = await self.client.get_chat(chat_id)
        return {
            'id': chat.id,
            'title': chat.title,
            'type': str(chat.type),
            'members_count': await self.client.get_chat_members_count(chat_id)
        }

# Initialize Telegram service
telegram_service = TelegramService(os.getenv("PYROGRAM_SESSION_STRING"))

@app.route('/send_message', methods=['POST'])
async def send_message():
    """API endpoint to send messages"""
    data = request.json
    chat_id = data.get('chat_id')
    message = data.get('message')
    
    if not chat_id or not message:
        return jsonify({'error': 'chat_id and message are required'}), 400
    
    try:
        message_id = await telegram_service.send_message(chat_id, message)
        return jsonify({'success': True, 'message_id': message_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat_info/<int:chat_id>')
async def get_chat_info(chat_id):
    """API endpoint to get chat information"""
    try:
        info = await telegram_service.get_chat_info(chat_id)
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
        print(code)
        print("-" * 60)
        
        print_warning("⚠️  IMPORTANT NOTES:")
        print("• Always validate session strings before using them")
        print("• Handle rate limiting and authentication errors")
        print("• Keep session strings secure and private")
        print("• Use proper logging for production applications")
        print("• Implement proper error handling and recovery")
        print("• Consider using session pools for high-volume applications")
