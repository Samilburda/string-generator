#!/usr/bin/env python3
"""
Pyrogram String Session Generator and Manager
Main application entry point with interactive CLI
"""

import asyncio
import sys
import os
from getpass import getpass
from session_manager import SessionManager
from session_validator import SessionValidator
from examples import SessionExamples
from utils import print_banner, print_success, print_error, print_warning, print_info

def print_menu():
    """Display the main menu options"""
    print("\n" + "="*60)
    print("PYROGRAM STRING SESSION MANAGER")
    print("="*60)
    print("1. Generate User Account Session String")
    print("2. Generate Bot Account Session String")
    print("3. Validate Existing Session String")
    print("4. Convert Session File to String")
    print("5. View Usage Examples")
    print("6. Security Best Practices")
    print("7. Exit")
    print("="*60)

def print_security_practices():
    """Display security best practices"""
    print("\n" + "="*60)
    print("SECURITY BEST PRACTICES")
    print("="*60)
    print("⚠️  IMPORTANT SECURITY WARNINGS:")
    print("1. Never share your session string publicly")
    print("2. Session strings provide FULL access to your account")
    print("3. Store session strings securely (encrypted files/environment variables)")
    print("4. Regularly rotate/regenerate session strings")
    print("5. Use different sessions for different applications")
    print("6. Monitor your account for unauthorized access")
    print("7. Keep your API credentials private")
    print("8. Use 2FA on your Telegram account")
    print("\n📝 BACKUP RECOMMENDATIONS:")
    print("1. Save session strings to multiple secure locations")
    print("2. Use encrypted storage solutions")
    print("3. Keep backups of your API credentials")
    print("4. Document which sessions are used for which purposes")
    print("="*60)

async def generate_user_session():
    """Generate session string for user account"""
    print_banner("USER ACCOUNT SESSION GENERATOR")
    
    # Get API credentials
    print("📋 Enter your API credentials from https://my.telegram.org/apps")
    try:
        api_id = input("API ID: ").strip()
        if not api_id:
            print_error("API ID cannot be empty!")
            return
        
        api_id = int(api_id)
        
        api_hash = input("API Hash: ").strip()
        if not api_hash:
            print_error("API Hash cannot be empty!")
            return
        
        # Optional phone number for faster login
        phone = input("Phone number (optional, press Enter to skip): ").strip()
        if phone and not phone.startswith('+'):
            phone = '+' + phone
        
        print_info("Starting session generation...")
        
        session_manager = SessionManager(api_id, api_hash)
        session_string = await session_manager.generate_user_session(phone if phone else None)
        
        if session_string:
            print_success("Session string generated successfully!")
            print("\n" + "="*60)
            print("YOUR SESSION STRING:")
            print("="*60)
            print(session_string)
            print("="*60)
            
            # Save to file
            filename = f"user_session_{api_id}.txt"
            with open(filename, 'w') as f:
                f.write(session_string)
            print_success(f"Session string saved to '{filename}'")
            
            # Option to send to saved messages
            send_to_saved = input("\nSend session string to your Saved Messages? (y/n): ").lower()
            if send_to_saved == 'y':
                await session_manager.send_to_saved_messages(session_string)
        
    except ValueError:
        print_error("API ID must be a valid number!")
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
    except Exception as e:
        print_error(f"Failed to generate session: {str(e)}")

async def generate_bot_session():
    """Generate session string for bot account"""
    print_banner("BOT ACCOUNT SESSION GENERATOR")
    
    try:
        bot_token = getpass("Bot Token (input hidden): ").strip()
        if not bot_token:
            print_error("Bot token cannot be empty!")
            return
        
        print_info("Starting bot session generation...")
        
        session_manager = SessionManager()
        session_string = await session_manager.generate_bot_session(bot_token)
        
        if session_string:
            print_success("Bot session string generated successfully!")
            print("\n" + "="*60)
            print("YOUR BOT SESSION STRING:")
            print("="*60)
            print(session_string)
            print("="*60)
            
            # Save to file
            filename = f"bot_session_{bot_token.split(':')[0]}.txt"
            with open(filename, 'w') as f:
                f.write(session_string)
            print_success(f"Bot session string saved to '{filename}'")
        
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
    except Exception as e:
        print_error(f"Failed to generate bot session: {str(e)}")

async def validate_session():
    """Validate an existing session string"""
    print_banner("SESSION STRING VALIDATOR")
    
    try:
        session_string = input("Enter session string to validate: ").strip()
        if not session_string:
            print_error("Session string cannot be empty!")
            return
        
        print_info("Validating session string...")
        
        validator = SessionValidator()
        is_valid, account_info = await validator.validate_session_string(session_string)
        
        if is_valid:
            print_success("Session string is valid!")
            if account_info:
                print_info(f"Account: {account_info}")
        else:
            print_error("Session string is invalid or expired!")
        
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
    except Exception as e:
        print_error(f"Failed to validate session: {str(e)}")

async def convert_session_file():
    """Convert existing session file to string"""
    print_banner("SESSION FILE TO STRING CONVERTER")
    
    try:
        session_name = input("Enter session name (without .session extension): ").strip()
        if not session_name:
            print_error("Session name cannot be empty!")
            return
        
        session_file = f"{session_name}.session"
        if not os.path.exists(session_file):
            print_error(f"Session file '{session_file}' not found!")
            return
        
        print_info("Converting session file to string...")
        
        session_manager = SessionManager()
        session_string = await session_manager.convert_session_file(session_name)
        
        if session_string:
            print_success("Session file converted successfully!")
            print("\n" + "="*60)
            print("CONVERTED SESSION STRING:")
            print("="*60)
            print(session_string)
            print("="*60)
            
            # Save to file
            filename = f"{session_name}_string.txt"
            with open(filename, 'w') as f:
                f.write(session_string)
            print_success(f"Session string saved to '{filename}'")
        
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
    except Exception as e:
        print_error(f"Failed to convert session file: {str(e)}")

def show_examples():
    """Display usage examples"""
    examples = SessionExamples()
    examples.display_all_examples()

async def main():
    """Main application loop"""
    print_banner("PYROGRAM STRING SESSION MANAGER")
    print("Welcome to the Pyrogram String Session Manager!")
    print("This tool helps you generate and manage Telegram session strings securely.")
    
    while True:
        try:
            print_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                await generate_user_session()
            elif choice == '2':
                await generate_bot_session()
            elif choice == '3':
                await validate_session()
            elif choice == '4':
                await convert_session_file()
            elif choice == '5':
                show_examples()
            elif choice == '6':
                print_security_practices()
            elif choice == '7':
                print_success("Thank you for using Pyrogram String Session Manager!")
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-7.")
                
        except KeyboardInterrupt:
            print_warning("\n\nExiting...")
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_warning("\nApplication terminated by user.")
        sys.exit(0)
