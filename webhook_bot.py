"""
Discord webhook bot for Facebook Marketplace phone monitoring
"""
import asyncio
import logging
import aiohttp
import json
from typing import Optional, Dict, List
from datetime import datetime

from config import Config
from monitor import FacebookMarketplaceMonitor
from utils import create_webhook_embed, is_valid_phone_listing

logger = logging.getLogger(__name__)

class DiscordWebhookBot:
    """Discord webhook bot for marketplace monitoring"""
    
    def __init__(self):
        # Validate configuration
        Config.validate_config()
        
        # Initialize monitor
        self.monitor = FacebookMarketplaceMonitor()
        self.monitoring_task: Optional[asyncio.Task] = None
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def initialize(self):
        """Initialize the webhook bot"""
        self.session = aiohttp.ClientSession()
        logger.info("Discord webhook bot initialized")
        
        # Start monitoring automatically
        await self.start_monitoring()
    
    async def send_webhook_message(self, embed_data: Dict):
        """
        Send a message to Discord via webhook
        
        Args:
            embed_data: Discord embed data to send
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        webhook_data = {
            "embeds": [embed_data],
            "username": "Marketplace Monitor",
            "avatar_url": "https://cdn.jsdelivr.net/npm/feather-icons@4.28.0/icons/smartphone.svg"
        }
        
        try:
            if not Config.DISCORD_WEBHOOK_URL:
                logger.error("Discord webhook URL not configured")
                return
                
            async with self.session.post(
                str(Config.DISCORD_WEBHOOK_URL),
                json=webhook_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 204:
                    logger.info("Successfully sent webhook message")
                else:
                    logger.error(f"Webhook failed with status {response.status}: {await response.text()}")
                    
        except Exception as e:
            logger.error(f"Error sending webhook: {e}")
    
    async def send_status_message(self, message: str, color: int = 0x0099ff):
        """
        Send a status message via webhook
        
        Args:
            message: Status message to send
            color: Embed color (default blue)
        """
        embed_data = {
            "title": "📱 Marketplace Monitor Status",
            "description": message,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "Facebook Marketplace Monitor"
            }
        }
        
        await self.send_webhook_message(embed_data)
    
    async def handle_new_listings(self, listings: List[Dict]):
        """
        Handle new listings found by the monitor
        
        Args:
            listings: List of new listings
        """
        try:
            for listing in listings:
                # Validate listing
                if not is_valid_phone_listing(listing):
                    continue
                
                # Create and send embed
                embed_data = create_webhook_embed(listing)
                await self.send_webhook_message(embed_data)
                
                logger.info(f"Sent webhook notification for listing: {listing.get('title', 'Unknown')}")
                
                # Small delay to avoid rate limits
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error handling new listings: {e}")
    
    async def start_monitoring(self):
        """Start the monitoring process"""
        if self.monitoring_task and not self.monitoring_task.done():
            logger.warning("Monitoring task is already running")
            return
        
        keywords = Config.get_search_keywords()
        
        # Send startup message
        await self.send_status_message(
            f"🚀 Monitoring started for {', '.join(Config.MONITORED_BRANDS)} phones!\n"
            f"⏰ Check interval: {Config.MONITOR_INTERVAL} seconds\n"
            f"💰 Price range: £{Config.MIN_PRICE} - £{Config.MAX_PRICE}",
            color=0x00ff00
        )
        
        self.monitoring_task = asyncio.create_task(
            self.monitor.start_monitoring(
                keywords=keywords,
                check_interval=Config.MONITOR_INTERVAL,
                callback=self.handle_new_listings
            )
        )
        
        logger.info("Monitoring task started")
    
    async def stop_monitoring(self):
        """Stop the monitoring process"""
        if self.monitoring_task:
            self.monitoring_task.cancel()
        
        self.monitor.stop_monitoring()
        
        await self.send_status_message(
            "⏹️ Monitoring stopped",
            color=0xff0000
        )
        
        logger.info("Monitoring stopped")
    
    async def get_status(self) -> Dict:
        """Get current monitoring status"""
        status = self.monitor.get_monitoring_status()
        
        status_message = (
            f"📊 **Current Status**\n"
            f"🔄 Status: {'Running' if status['is_monitoring'] else 'Stopped'}\n"
            f"⏰ Last Check: {status['last_check']}\n"
            f"📱 Total Listings Seen: {status['total_seen_listings']}\n"
            f"📍 Monitored Brands: {', '.join(Config.MONITORED_BRANDS)}"
        )
        
        await self.send_status_message(status_message)
        return status
    
    async def close(self):
        """Close the webhook bot and clean up"""
        if self.monitoring_task:
            self.monitoring_task.cancel()
        
        if self.session:
            await self.session.close()
        
        logger.info("Webhook bot closed")