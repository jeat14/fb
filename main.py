"""
Main entry point for the Discord Facebook Marketplace Monitor Bot
"""
import asyncio
import logging
from webhook_bot import DiscordWebhookBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    """Main function to start the Discord webhook bot"""
    bot = DiscordWebhookBot()
    try:
        await bot.initialize()
        
        # Keep the bot running
        while True:
            await asyncio.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot crashed with error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())