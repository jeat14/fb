"""
Facebook Marketplace connector for enhanced listing retrieval
"""
import aiohttp
import asyncio
import logging
import random
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class FacebookMarketplaceConnector:
    """Enhanced connector for Facebook Marketplace listings"""
    
    def __init__(self):
        self.session = None
        
    async def get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            connector = aiohttp.TCPConnector(limit=10)
            timeout = aiohttp.ClientTimeout(total=30)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-GB,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers=headers
            )
        return self.session
    
    async def search_marketplace(self, search_terms: List[str]) -> List[Dict]:
        """
        Search Facebook Marketplace for listings
        
        Args:
            search_terms: List of search terms
            
        Returns:
            List of sample listings (simulated for development)
        """
        logger.info(f"Searching Facebook Marketplace for: {search_terms}")
        
        # Generate realistic UK phone listings for development
        return self.generate_sample_uk_listings()
    
    def generate_sample_uk_listings(self) -> List[Dict]:
        """Generate sample UK phone listings for development"""
        listings = []
        
        # iPhone listings
        iphone_listings = [
            {
                "title": "iPhone 14 128GB Blue - Unlocked, Excellent Condition",
                "price": "£185",
                "location": "London, Greater London",
                "description": "iPhone 14 in excellent condition, only 6 months old. Unlocked to all networks. Comes with original box, charger, and unused EarPods. No scratches or damage. Battery health 98%.",
                "url": "https://facebook.com/marketplace/item/iphone14sample",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "iPhone 13 Pro 256GB Graphite - Very Good Condition",
                "price": "£195",
                "location": "Birmingham, West Midlands",
                "description": "iPhone 13 Pro with 256GB storage. Very good condition with minor wear on edges. Screen is perfect. Unlocked. Includes case and screen protector already applied.",
                "url": "https://facebook.com/marketplace/item/iphone13pro",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "iPhone 12 64GB White - Good Condition, Unlocked",
                "price": "£140",
                "location": "Manchester, Greater Manchester",
                "description": "iPhone 12 in good working condition. Some light scratches on back but screen is pristine. Unlocked to all networks. Battery health 89%. Bargain price!",
                "url": "https://facebook.com/marketplace/item/iphone12white",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "iPhone SE 2022 128GB Red - Like New",
                "price": "£160",
                "location": "Leeds, West Yorkshire", 
                "description": "iPhone SE 3rd generation in like new condition. Barely used, kept in case since day one. Unlocked, comes with original packaging and accessories.",
                "url": "https://facebook.com/marketplace/item/iphonese2022",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        # Samsung listings
        samsung_listings = [
            {
                "title": "Samsung Galaxy S23 128GB Lavender - Pristine Condition",
                "price": "£190",
                "location": "Glasgow, Scotland",
                "description": "Samsung Galaxy S23 in pristine condition. Used for only 2 months. Unlocked to all networks. Comes with wireless charger and premium case worth £40. Amazing camera quality.",
                "url": "https://facebook.com/marketplace/item/galaxys23",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "Samsung Galaxy S22 256GB Black - Excellent Condition",
                "price": "£175",
                "location": "Liverpool, Merseyside",
                "description": "Galaxy S22 with 256GB storage. Excellent condition, always kept in case. Unlocked. Great performance and camera. Includes original charger and box.",
                "url": "https://facebook.com/marketplace/item/galaxys22black",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "Samsung Galaxy A54 5G 256GB Awesome Graphite",
                "price": "£130",
                "location": "Newcastle, Tyne and Wear",
                "description": "Galaxy A54 5G with 256GB storage. Great mid-range phone with excellent camera and battery life. Minor wear but fully functional. Unlocked.",
                "url": "https://facebook.com/marketplace/item/galaxya54",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "Samsung Galaxy S21 128GB Phantom Gray - Good Condition",
                "price": "£155",
                "location": "Bristol, England",
                "description": "Galaxy S21 in good condition. Some minor scratches but screen is perfect. Unlocked to all networks. Still runs smoothly. Great value for money.",
                "url": "https://facebook.com/marketplace/item/galaxys21",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        # Mix the listings and add some randomization
        all_listings = iphone_listings + samsung_listings
        
        # Randomly select 4-6 listings to simulate real search results
        selected_count = random.randint(4, 6)
        selected_listings = random.sample(all_listings, min(selected_count, len(all_listings)))
        
        logger.info(f"Generated {len(selected_listings)} sample UK phone listings")
        return selected_listings
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()