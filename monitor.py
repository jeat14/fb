"""
Facebook Marketplace monitor for phone listings
"""
import asyncio
import logging
import re
from typing import List, Dict, Set
from datetime import datetime, timedelta
import hashlib
from web_scraper import FacebookMarketplaceScraper
from facebook_connector import FacebookMarketplaceConnector
from config import Config

logger = logging.getLogger(__name__)

class FacebookMarketplaceMonitor:
    """Monitor Facebook Marketplace for phone listings"""
    
    def __init__(self):
        self.seen_listings: Set[str] = set()
        self.last_check = datetime.now() - timedelta(hours=1)
        self.is_monitoring = False
        self.scraper = FacebookMarketplaceScraper()
        self.connector = FacebookMarketplaceConnector()
        
    def generate_listing_id(self, listing: Dict) -> str:
        """
        Generate a unique ID for a listing based on its content
        
        Args:
            listing: Dictionary containing listing information
            
        Returns:
            Unique string ID for the listing
        """
        content = f"{listing.get('title', '')}{listing.get('price', '')}{listing.get('location', '')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def fetch_marketplace_listings(self, keywords: List[str]) -> List[Dict]:
        """
        Fetch listings from Facebook Marketplace using web scraping
        
        Args:
            keywords: List of search keywords
            
        Returns:
            List of listing dictionaries
        """
        logger.info(f"Searching Facebook Marketplace for phone listings...")
        
        try:
            # Use the enhanced Facebook connector for better results
            search_terms = ["iPhone", "Samsung Galaxy"]
            all_listings = await self.connector.search_marketplace(search_terms)
            
            logger.info(f"Total listings found: {len(all_listings)}")
            return all_listings
            
        except Exception as e:
            logger.error(f"Error in fetch_marketplace_listings: {e}")
            return []
    
    def filter_listings(self, listings: List[Dict], keywords: List[str]) -> List[Dict]:
        """
        Filter listings based on phone-specific criteria and UK price under £200
        
        Args:
            listings: List of raw listings
            keywords: List of search keywords
            
        Returns:
            List of filtered listings under £200
        """
        filtered = []
        
        for listing in listings:
            title = listing.get("title", "").lower()
            description = listing.get("description", "").lower()
            combined_text = f"{title} {description}"
            price_str = listing.get("price", "")
            
            # Check if listing matches phone keywords
            matches_keyword = any(keyword.lower() in combined_text for keyword in keywords)
            
            if not matches_keyword:
                continue
                
            # Extract price for filtering - prioritize UK pounds
            price_match = re.search(r'[\£](\d+)', price_str)
            if not price_match:
                # Try other currency symbols as fallback
                price_match = re.search(r'[\$€]?(\d+)', price_str)
            
            if price_match:
                price = int(price_match.group(1))
                # Only show phones under £200
                if price < Config.MIN_PRICE or price > Config.MAX_PRICE:
                    logger.debug(f"Filtered out listing: {title[:30]} - Price: {price_str} (outside £{Config.MIN_PRICE}-£{Config.MAX_PRICE} range)")
                    continue
            else:
                # Skip listings without clear pricing
                logger.debug(f"Filtered out listing: {title[:30]} - No clear price found")
                continue
            
            # Filter out obvious non-phone items
            exclude_terms = ['case', 'cover', 'charger', 'cable', 'screen protector', 'warranty', 'accessories']
            if any(term in title for term in exclude_terms):
                logger.debug(f"Filtered out non-phone item: {title[:30]}")
                continue
                
            # Ensure price is displayed in £
            if not price_str.startswith('£'):
                listing['price'] = f"£{price}"
                
            filtered.append(listing)
            logger.debug(f"Listing matched criteria: {listing.get('title', 'Unknown title')}")
        
        logger.info(f"Filtered to {len(filtered)} phone listings under £{Config.MAX_PRICE}")
        return filtered
    
    def get_new_listings(self, listings: List[Dict]) -> List[Dict]:
        """
        Filter out listings that have already been seen
        
        Args:
            listings: List of all listings
            
        Returns:
            List of new listings only
        """
        new_listings = []
        
        # Reset seen listings periodically to catch new versions of similar listings
        if len(self.seen_listings) > 1000:  # Reset after 1000 seen listings
            logger.info("Resetting seen listings cache to catch new items")
            self.seen_listings.clear()
        
        for listing in listings:
            listing_id = self.generate_listing_id(listing)
            
            if listing_id not in self.seen_listings:
                self.seen_listings.add(listing_id)
                new_listings.append(listing)
                logger.info(f"New listing found: {listing.get('title', 'Unknown title')}")
        
        # If no new listings and this is startup, send a few listings for testing
        if len(new_listings) == 0 and len(self.seen_listings) < 5 and len(listings) > 0:
            logger.info(f"Sending first 2 listings as notifications for testing from {len(listings)} available...")
            test_listings = listings[:2]
            # Mark these as seen so they don't repeat constantly
            for listing in test_listings:
                test_id = self.generate_listing_id(listing)
                self.seen_listings.add(test_id)
                logger.info(f"Adding test listing: {listing.get('title', 'Unknown')[:50]}...")
            return test_listings
        
        return new_listings
    
    async def check_for_new_listings(self, keywords: List[str]) -> List[Dict]:
        """
        Check for new phone listings
        
        Args:
            keywords: List of search keywords
            
        Returns:
            List of new listings
        """
        try:
            logger.info("Checking for new phone listings...")
            
            # Fetch all listings
            all_listings = await self.fetch_marketplace_listings(keywords)
            
            # Filter for phone listings
            phone_listings = self.filter_listings(all_listings, keywords)
            
            # Get only new listings
            new_listings = self.get_new_listings(phone_listings)
            
            self.last_check = datetime.now()
            
            if len(new_listings) > 0:
                logger.info(f"Found {len(new_listings)} new phone listings")
                for listing in new_listings:
                    logger.info(f"New listing: {listing.get('title', 'Unknown')[:50]}...")
            else:
                logger.info(f"Found {len(new_listings)} new phone listings")
            
            return new_listings
            
        except Exception as e:
            logger.error(f"Error checking for new listings: {e}")
            return []
    
    async def start_monitoring(self, keywords: List[str], check_interval: int, callback):
        """
        Start continuous monitoring for new listings
        
        Args:
            keywords: List of search keywords
            check_interval: Time between checks in seconds
            callback: Async function to call when new listings are found
        """
        self.is_monitoring = True
        logger.info(f"Starting monitoring with {check_interval} second intervals")
        
        while self.is_monitoring:
            try:
                new_listings = await self.check_for_new_listings(keywords)
                
                if new_listings:
                    await callback(new_listings)
                
                # Wait for next check
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    def stop_monitoring(self):
        """Stop the monitoring process"""
        self.is_monitoring = False
        logger.info("Monitoring stopped")
    
    def get_monitoring_status(self) -> Dict:
        """
        Get current monitoring status
        
        Returns:
            Dictionary with monitoring status information
        """
        return {
            "is_monitoring": self.is_monitoring,
            "last_check": self.last_check.isoformat(),
            "total_seen_listings": len(self.seen_listings)
        }