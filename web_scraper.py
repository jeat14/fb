"""
Facebook Marketplace web scraper using trafilatura
"""
import aiohttp
import asyncio
import logging
import trafilatura
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class FacebookMarketplaceScraper:
    """Scraper for Facebook Marketplace phone listings"""
    
    def __init__(self):
        self.session = None
        
    async def get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
        return self.session
    
    async def scrape_marketplace_listings(self, search_terms: List[str]) -> List[Dict]:
        """
        Scrape Facebook Marketplace for phone listings
        
        Args:
            search_terms: List of search terms like ['iPhone', 'Samsung Galaxy']
            
        Returns:
            List of listing dictionaries
        """
        session = await self.get_session()
        all_listings = []
        
        for search_term in search_terms:
            try:
                # Generate sample listings for development/testing
                listings = self.generate_sample_listings(search_term)
                all_listings.extend(listings)
                
                logger.info(f"Generated {len(listings)} sample listings for '{search_term}'")
                
            except Exception as e:
                logger.error(f"Error scraping for term '{search_term}': {e}")
                continue
        
        return all_listings
    
    def generate_sample_listings(self, search_term: str) -> List[Dict]:
        """Generate sample listings for development"""
        listings = []
        
        if "iphone" in search_term.lower():
            listings.extend([
                {
                    "title": "iPhone 13 128GB Unlocked - Excellent Condition",
                    "price": "£180",
                    "location": "London, UK",
                    "description": "iPhone 13 in excellent condition, barely used. Unlocked to all networks. Comes with original charger and box.",
                    "url": "https://facebook.com/marketplace/item/sample1",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "title": "iPhone 12 64GB - Good Condition",
                    "price": "£150",
                    "location": "Birmingham, UK", 
                    "description": "iPhone 12 in good working condition. Some minor scratches on back but screen is perfect. Unlocked.",
                    "url": "https://facebook.com/marketplace/item/sample2",
                    "timestamp": datetime.now().isoformat()
                }
            ])
        
        if "samsung" in search_term.lower():
            listings.extend([
                {
                    "title": "Samsung Galaxy S22 128GB - Like New",
                    "price": "£190",
                    "location": "Manchester, UK",
                    "description": "Samsung Galaxy S22 in pristine condition. Used for 3 months only. Unlocked, comes with case and screen protector.",
                    "url": "https://facebook.com/marketplace/item/sample3",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "title": "Samsung Galaxy A54 5G 256GB",
                    "price": "£120",
                    "location": "Leeds, UK",
                    "description": "Samsung Galaxy A54 5G with 256GB storage. Great camera and battery life. Minor wear but fully functional.",
                    "url": "https://facebook.com/marketplace/item/sample4",
                    "timestamp": datetime.now().isoformat()
                }
            ])
        
        return listings
    
    def parse_marketplace_content(self, content: str, search_term: str) -> List[Dict]:
        """
        Parse extracted marketplace content for phone listings
        
        Args:
            content: Extracted text content from trafilatura
            search_term: The search term used
            
        Returns:
            List of parsed listings
        """
        listings = []
        
        # This would contain actual parsing logic for real Facebook content
        # For now, return sample data
        
        return listings
    
    def is_valid_phone_listing(self, listing: Dict) -> bool:
        """
        Check if a listing appears to be a valid phone listing
        
        Args:
            listing: Listing dictionary
            
        Returns:
            Boolean indicating validity
        """
        title = listing.get('title', '').lower()
        description = listing.get('description', '').lower()
        
        # Check for phone-related terms
        phone_terms = ['iphone', 'samsung', 'galaxy', 'phone', 'smartphone']
        has_phone_term = any(term in f"{title} {description}" for term in phone_terms)
        
        # Check for price
        has_price = bool(listing.get('price'))
        
        return has_phone_term and has_price
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()