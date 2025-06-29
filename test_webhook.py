"""
Test webhook functionality
"""
import asyncio
import aiohttp
from config import Config
from utils import create_webhook_embed

async def test_webhook():
    """Send a test message to Discord webhook"""
    
    # Test listing data
    test_listing = {
        "title": "Test iPhone 13 128GB - Excellent Condition",
        "price": "£175",
        "location": "London, UK",
        "description": "This is a test notification to verify your Discord webhook is working properly. iPhone 13 in excellent condition with 128GB storage.",
        "url": "https://facebook.com/marketplace/test",
        "timestamp": "2025-06-29T12:00:00Z"
    }
    
    # Create webhook embed
    embed_data = create_webhook_embed(test_listing)
    
    webhook_data = {
        "embeds": [embed_data],
        "username": "Marketplace Monitor (Test)",
        "avatar_url": "https://cdn.jsdelivr.net/npm/feather-icons@4.28.0/icons/smartphone.svg"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                Config.DISCORD_WEBHOOK_URL,
                json=webhook_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 204:
                    print("✅ Test webhook sent successfully!")
                    print("Check your Discord channel for the test notification.")
                else:
                    print(f"❌ Webhook failed with status {response.status}")
                    print(await response.text())
        except Exception as e:
            print(f"❌ Error sending test webhook: {e}")

if __name__ == "__main__":
    asyncio.run(test_webhook())