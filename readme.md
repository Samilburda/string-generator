# Pyrogram String Session Manager

A comprehensive Python application for generating and managing Pyrogram session strings for Telegram bots and user accounts.

## Features

- **User Account Session Generation**: Generate session strings for Telegram user accounts
- **Bot Account Session Generation**: Generate session strings for Telegram bots
- **Session Validation**: Validate existing session strings
- **Session File Conversion**: Convert existing .session files to session strings
- **Interactive CLI**: User-friendly command-line interface with colored output
- **Security Best Practices**: Built-in security warnings and guidelines
- **Usage Examples**: Comprehensive code examples for different use cases

## Installation

1. **Clone or download the project files**

2. **Install required dependencies**:
   ```bash
   pip install pyrogram colorama python-dotenv
   ```

3. **Optional: Install TgCrypto for better performance**:
   ```bash
   pip install tgcrypto
   ```

## Quick Start

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Choose from the menu options**:
   - Generate User Account Session String
   - Generate Bot Account Session String
   - Validate Existing Session String
   - Convert Session File to String
   - View Usage Examples
   - Security Best Practices

## Prerequisites

### For User Account Sessions:
- **API ID** and **API Hash** from [my.telegram.org](https://my.telegram.org/apps)
- **Phone number** registered with Telegram
- **Verification code** (sent via SMS/call)

### For Bot Sessions:
- **Bot token** from [@BotFather](https://t.me/BotFather)

## Usage Examples

### Basic User Session Usage

```python
from pyrogram import Client
import asyncio

async def main():
    # Your session string
    session_string = "your_session_string_here"
    
    # Create client
    app = Client(
        name="my_app",
        session_string=session_string
    )
    
    async with app:
        # Get account info
        me = await app.get_me()
        print(f"Logged in as: {me.first_name}")
        
        # Send message
        await app.send_message("me", "Hello from session string!")

if __name__ == "__main__":
    asyncio.run(main())
```

### Bot Session Usage

```python
from pyrogram import Client
import asyncio

async def main():
    # Your bot session string
    bot_session = "your_bot_session_string_here"
    
    # Create bot client
    bot = Client(
        name="my_bot",
        session_string=bot_session
    )
    
    async with bot:
        # Get bot info
        me = await bot.get_me()
        print(f"Bot: {me.first_name} (@{me.username})")
        
        # Handle messages
        @bot.on_message()
        async def handle_message(client, message):
            if message.text == "/start":
                await message.reply("Hello! I'm running with session string!")
        
        # Keep bot running
        await bot.idle()

if __name__ == "__main__":
    asyncio.run(main())
```

### Error Handling

```python
from pyrogram import Client
from pyrogram.errors import AuthKeyUnregistered, FloodWait
import asyncio

async def safe_session_usage(session_string):
    try:
        app = Client(
            name="safe_app",
            session_string=session_string
        )
        
        await app.start()
        print("✅ Successfully connected!")
        
        # Your app logic here
        await app.send_message("me", "Session is working!")
        
        await app.stop()
        
    except AuthKeyUnregistered:
        print("❌ Session string is invalid or expired!")
    except FloodWait as e:
        print(f"❌ Rate limited! Wait {e.value} seconds")
    except Exception as e:
        print(f"❌ Error: {e}")

# Usage
asyncio.run(safe_session_usage("your_session_string"))
```

## Security Best Practices

### 🔐 Critical Security Guidelines

1. **Never share session strings** - They provide full access to your account
2. **Store securely** - Use environment variables or encrypted storage
3. **Use different sessions** - For different applications/purposes
4. **Monitor access** - Check for unauthorized account activity
5. **Rotate regularly** - Generate new session strings periodically
6. **Enable 2FA** - On your Telegram account for extra security

### 📝 Storage Recommendations

```python
# Use environment variables
import os
from pyrogram import Client

session_string = os.getenv("PYROGRAM_SESSION_STRING")

# Or use .env files
from dotenv import load_dotenv
load_dotenv()

session_string = os.getenv("PYROGRAM_SESSION_STRING")
```

## Configuration

### Environment Variables

Create a `.env` file in your project directory:

```env
# API Credentials (optional defaults)
PYROGRAM_API_ID=your_api_id
PYROGRAM_API_HASH=your_api_hash

# Session Configuration
SESSION_NAME_PREFIX=my_app_session
SESSION_BACKUP_DIR=./backups
CREATE_BACKUPS=true
SEND_TO_SAVED_MESSAGES=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=session_manager.log

# Security
ENABLE_2FA_WARNING=true
ENABLE_BACKUP_ENCRYPTION=false
```

## File Structure

```
pyrogram-session-manager/
├── main.py                 # Main application entry point
├── session_manager.py      # Session generation logic
├── session_validator.py    # Session validation
├── config.py              # Configuration management
├── examples.py            # Usage examples
├── utils.py               # Utility functions
├── demo_usage.py          # Demo script
├── README.md              # This file
├── backups/               # Session backups (auto-created)
├── logs/                  # Application logs (auto-created)
└── exports/               # Exported sessions (auto-created)
```

## Advanced Features

### Multiple Session Management

```python
from session_validator import SessionValidator

async def validate_multiple_sessions():
    validator = SessionValidator()
    
    session_strings = [
        "session_string_1",
        "session_string_2",
        "session_string_3"
    ]
    
    results = await validator.validate_multiple_sessions(session_strings)
    
    for i, result in results.items():
        print(f"Session {i+1}: {'✅ Valid' if result['is_valid'] else '❌ Invalid'}")
```

### Session Permissions Check

```python
from session_validator import SessionValidator

async def check_permissions():
    validator = SessionValidator()
    
    permissions = await validator.check_session_permissions(session_string)
    
    if permissions:
        print("Session Permissions:")
        for perm, value in permissions.items():
            print(f"  {perm}: {'✅' if value else '❌'}")
```

## Troubleshooting

### Common Issues

1. **"Invalid API ID"**
   - Check your API ID from my.telegram.org
   - Ensure it's a valid number

2. **"Session Password Needed"**
   - 2FA is enabled on your account
   - Temporarily disable 2FA or use a different method

3. **"Rate Limited"**
   - Wait the specified time before retrying
   - Implement proper rate limiting in your code

4. **"Session Expired"**
   - Generate a new session string
   - Check if your account was logged out

### Performance Tips

1. **Install TgCrypto**: `pip install tgcrypto`
2. **Use in-memory sessions** for temporary operations
3. **Implement connection pooling** for multiple sessions
4. **Handle rate limits properly** with exponential backoff

## Demo Script

Run the included demo script to test your session strings:

```bash
python demo_usage.py
```

This will demonstrate:
- Basic connection and authentication
- Sending messages to saved messages
- Retrieving account information
- File operations
- Error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the security best practices
3. Test with the demo script
4. Check Pyrogram documentation: https://docs.pyrogram.org

## Disclaimer

This tool is for educational and legitimate use only. Users are responsible for complying with Telegram's Terms of Service and applicable laws. Always keep your session strings secure and never share them with others.