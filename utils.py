"""
Utility functions for the Pyrogram Session Manager
"""

import os
import sys
from datetime import datetime
import colorama
from colorama import Fore, Style, Back

# Initialize colorama for cross-platform colored output
colorama.init()

def print_banner(title):
    """Print a styled banner"""
    print("\n" + "="*60)
    print(f"{Fore.CYAN}{Style.BRIGHT}{title.center(60)}{Style.RESET_ALL}")
    print("="*60)

def print_success(message):
    """Print success message in green"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    """Print error message in red"""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info message in blue"""
    print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")

def print_highlight(message):
    """Print highlighted message"""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}✨ {message}{Style.RESET_ALL}")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt, input_type=str, required=True):
    """
    Get user input with validation
    
    Args:
        prompt (str): Input prompt
        input_type (type): Expected input type
        required (bool): Whether input is required
        
    Returns:
        Input value or None if not required and empty
    """
    while True:
        try:
            value = input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()
            
            if not value and not required:
                return None
            
            if not value and required:
                print_error("This field is required!")
                continue
            
            if input_type == int:
                return int(value)
            elif input_type == float:
                return float(value)
            else:
                return value
                
        except ValueError:
            print_error(f"Invalid input! Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print_warning("\nOperation cancelled.")
            return None

def format_file_size(size_bytes):
    """
    Format file size in human readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_phone_number(phone):
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid format
    """
    if not phone:
        return False
    
    # Remove spaces and common separators
    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Check if it starts with + or is all digits
    if phone.startswith("+"):
        phone = phone[1:]
    
    # Should be all digits and reasonable length
    return phone.isdigit() and 7 <= len(phone) <= 15

def validate_api_credentials(api_id, api_hash):
    """
    Validate API credentials format
    
    Args:
        api_id (str): API ID
        api_hash (str): API Hash
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Validate API ID
    try:
        api_id_int = int(api_id)
        if api_id_int <= 0:
            return False, "API ID must be a positive number"
    except ValueError:
        return False, "API ID must be a valid number"
    
    # Validate API Hash
    if not api_hash or len(api_hash) < 32:
        return False, "API Hash must be at least 32 characters long"
    
    if not all(c.isalnum() for c in api_hash):
        return False, "API Hash should contain only alphanumeric characters"
    
    return True, "Valid"

def validate_bot_token(token):
    """
    Validate bot token format
    
    Args:
        token (str): Bot token to validate
        
    Returns:
        bool: True if valid format
    """
    if not token:
        return False
    
    # Basic format: numbers:alphanumeric_string
    parts = token.split(':')
    if len(parts) != 2:
        return False
    
    # First part should be numbers (bot ID)
    if not parts[0].isdigit():
        return False
    
    # Second part should be alphanumeric and reasonable length
    if len(parts[1]) < 35:
        return False
    
    return True

def create_backup_filename(base_name, extension="txt"):
    """
    Create a backup filename with timestamp
    
    Args:
        base_name (str): Base filename
        extension (str): File extension
        
    Returns:
        str: Backup filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_backup_{timestamp}.{extension}"

def safe_write_file(filename, content, backup=True):
    """
    Safely write content to file with optional backup
    
    Args:
        filename (str): Target filename
        content (str): Content to write
        backup (bool): Whether to create backup if file exists
        
    Returns:
        bool: True if successful
    """
    try:
        # Create backup if file exists
        if backup and os.path.exists(filename):
            backup_name = create_backup_filename(filename.rsplit('.', 1)[0])
            os.rename(filename, backup_name)
            print_info(f"Created backup: {backup_name}")
        
        # Write content
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print_error(f"Failed to write file: {str(e)}")
        return False

def get_file_info(filepath):
    """
    Get file information
    
    Args:
        filepath (str): Path to file
        
    Returns:
        dict: File information
    """
    try:
        stat = os.stat(filepath)
        return {
            'size': stat.st_size,
            'size_formatted': format_file_size(stat.st_size),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'exists': True
        }
    except Exception:
        return {'exists': False}

def print_progress_bar(current, total, width=50):
    """
    Print a progress bar
    
    Args:
        current (int): Current progress
        total (int): Total progress
        width (int): Width of progress bar
    """
    if total == 0:
        return
    
    progress = current / total
    filled = int(width * progress)
    bar = '█' * filled + '░' * (width - filled)
    percentage = progress * 100
    
    print(f"\r{Fore.GREEN}Progress: |{bar}| {percentage:.1f}% ({current}/{total}){Style.RESET_ALL}", end='')
    
    if current == total:
        print()  # New line when complete

def confirm_action(message, default=False):
    """
    Ask for user confirmation
    
    Args:
        message (str): Confirmation message
        default (bool): Default answer if user just presses enter
        
    Returns:
        bool: True if confirmed
    """
    suffix = "[Y/n]" if default else "[y/N]"
    response = input(f"{Fore.YELLOW}{message} {suffix}: {Style.RESET_ALL}").strip().lower()
    
    if not response:
        return default
    
    return response in ['y', 'yes', 'true', '1']

def print_table(headers, rows):
    """
    Print a formatted table
    
    Args:
        headers (list): Table headers
        rows (list): Table rows
    """
    if not rows:
        print_info("No data to display")
        return
    
    # Calculate column widths
    col_widths = [len(str(header)) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print header
    header_row = " | ".join(str(header).ljust(col_widths[i]) for i, header in enumerate(headers))
    print(f"{Fore.CYAN}{header_row}{Style.RESET_ALL}")
    print("-" * len(header_row))
    
    # Print rows
    for row in rows:
        row_str = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(row_str)
