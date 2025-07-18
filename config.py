"""
Configuration settings for Pyrogram Session Manager
"""

import os
from datetime import datetime
from typing import Optional

class Config:
    """Configuration class for the application"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """Load configuration from environment variables"""
        
        # API Configuration
        self.DEFAULT_API_ID = os.getenv("PYROGRAM_API_ID")
        self.DEFAULT_API_HASH = os.getenv("PYROGRAM_API_HASH")
        
        # Session Configuration
        self.SESSION_NAME_PREFIX = os.getenv("SESSION_NAME_PREFIX", "pyrogram_session")
        self.SESSION_BACKUP_DIR = os.getenv("SESSION_BACKUP_DIR", "./backups")
        
        # Application Configuration
        self.APP_NAME = "Pyrogram Session Manager"
        self.APP_VERSION = "1.0.0"
        self.APP_DESCRIPTION = "Professional Pyrogram string session generator and manager"
        
        # Logging Configuration
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "session_manager.log")
        
        # Security Configuration
        self.ENABLE_2FA_WARNING = os.getenv("ENABLE_2FA_WARNING", "true").lower() == "true"
        self.ENABLE_BACKUP_ENCRYPTION = os.getenv("ENABLE_BACKUP_ENCRYPTION", "false").lower() == "true"
        
        # Rate Limiting
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
        self.RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))
        
        # File Configuration
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "txt,json,session").split(",")
        
        # Create directories if they don't exist
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories"""
        directories = [
            self.SESSION_BACKUP_DIR,
            "./logs",
            "./exports"
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
    
    def get_current_timestamp(self) -> str:
        """Get current timestamp as string"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_current_date(self) -> str:
        """Get current date as string"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_backup_filename(self, base_name: str, extension: str = "txt") -> str:
        """Generate backup filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_backup_{timestamp}.{extension}"
    
    def get_export_filename(self, account_type: str, identifier: str) -> str:
        """Generate export filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{account_type}_session_{identifier}_{timestamp}.txt"
    
    def get_log_filename(self) -> str:
        """Get log filename with date"""
        date = datetime.now().strftime("%Y%m%d")
        return f"session_manager_{date}.log"
    
    def validate_api_credentials(self, api_id: Optional[str], api_hash: Optional[str]) -> tuple:
        """
        Validate API credentials
        
        Args:
            api_id: API ID to validate
            api_hash: API Hash to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not api_id:
            return False, "API ID is required"
        
        if not api_hash:
            return False, "API Hash is required"
        
        try:
            api_id_int = int(api_id)
            if api_id_int <= 0:
                return False, "API ID must be a positive number"
        except ValueError:
            return False, "API ID must be a valid number"
        
        if len(api_hash) < 32:
            return False, "API Hash must be at least 32 characters long"
        
        return True, "Valid credentials"
    
    def get_session_file_path(self, session_name: str) -> str:
        """Get full path for session file"""
        return os.path.join(".", f"{session_name}.session")
    
    def get_backup_file_path(self, filename: str) -> str:
        """Get full path for backup file"""
        return os.path.join(self.SESSION_BACKUP_DIR, filename)
    
    def get_export_file_path(self, filename: str) -> str:
        """Get full path for export file"""
        return os.path.join("./exports", filename)
    
    def get_app_info(self) -> dict:
        """Get application information"""
        return {
            'name': self.APP_NAME,
            'version': self.APP_VERSION,
            'description': self.APP_DESCRIPTION,
            'author': 'Pyrogram Session Manager Team',
            'license': 'MIT',
            'python_version': '3.7+',
            'pyrogram_version': '2.0+',
            'created': self.get_current_timestamp()
        }
    
    def get_security_warnings(self) -> list:
        """Get security warnings to display"""
        warnings = [
            "Never share your session string with anyone",
            "Session strings provide full access to your account",
            "Store session strings in secure, encrypted locations",
            "Regularly rotate and update your session strings",
            "Monitor your account for unauthorized access",
            "Use strong, unique passwords for your Telegram account",
            "Enable two-factor authentication on your account",
            "Keep your API credentials private and secure"
        ]
        
        return warnings
    
    def get_usage_tips(self) -> list:
        """Get usage tips"""
        tips = [
            "Use environment variables to store sensitive data",
            "Test session strings before using them in production",
            "Keep backups of your session strings in multiple locations",
            "Use different sessions for different applications",
            "Implement proper error handling in your applications",
            "Monitor your application logs for errors and warnings",
            "Use rate limiting to avoid hitting API limits",
            "Consider using session pools for high-volume applications"
        ]
        
        return tips
    
    def get_supported_formats(self) -> dict:
        """Get supported export formats"""
        return {
            'txt': 'Plain text file',
            'json': 'JSON format with metadata',
            'env': 'Environment variable format',
            'yaml': 'YAML configuration format'
        }
    
    def get_telegram_limits(self) -> dict:
        """Get Telegram API limits"""
        return {
            'messages_per_second': 30,
            'messages_per_minute': 20,
            'bulk_messages_per_minute': 5,
            'chats_per_minute': 200,
            'members_per_minute': 200
        }
    
    def should_create_backup(self) -> bool:
        """Check if backup should be created"""
        return os.getenv("CREATE_BACKUPS", "true").lower() == "true"
    
    def should_send_to_saved_messages(self) -> bool:
        """Check if session should be sent to saved messages"""
        return os.getenv("SEND_TO_SAVED_MESSAGES", "true").lower() == "true"
    
    def get_default_session_name(self) -> str:
        """Get default session name"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.SESSION_NAME_PREFIX}_{timestamp}"
