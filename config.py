"""
Configuration settings for the Discord webhook bot
"""
import os
from typing import List

class Config:
    """Configuration class for bot settings"""
    
    # Discord Webhook URL - required
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    
    # Monitoring settings
    MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", "30"))  # 30 seconds default
    
    # Supported phone brands
    MONITORED_BRANDS = ["iPhone", "Samsung"]
    
    # Price range filters (optional)
    MIN_PRICE = int(os.getenv("MIN_PRICE", "0"))
    MAX_PRICE = int(os.getenv("MAX_PRICE", "200"))
    
    # Location filter (optional)
    LOCATION_FILTER = os.getenv("LOCATION_FILTER", "")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.DISCORD_WEBHOOK_URL:
            raise ValueError("DISCORD_WEBHOOK_URL environment variable is required")
        
        return True
    
    @classmethod
    def get_search_keywords(cls) -> List[str]:
        """Get search keywords for phone monitoring"""
        keywords = []
        for brand in cls.MONITORED_BRANDS:
            if brand.lower() == "iphone":
                keywords.extend([
                    "iPhone 15", "iPhone 14", "iPhone 13", "iPhone 12", 
                    "iPhone 11", "iPhone XS", "iPhone XR", "iPhone X",
                    "iPhone SE", "iPhone Pro", "iPhone Plus", "iPhone Mini"
                ])
            elif brand.lower() == "samsung":
                keywords.extend([
                    "Samsung Galaxy S24", "Samsung Galaxy S23", "Samsung Galaxy S22",
                    "Samsung Galaxy S21", "Samsung Galaxy Note", "Samsung Galaxy A",
                    "Samsung Galaxy Z", "Galaxy S24", "Galaxy S23", "Galaxy S22"
                ])
        return keywords