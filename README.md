# Discord Facebook Marketplace Phone Monitor Bot

A Python bot that monitors Facebook Marketplace UK for budget phone deals under £200 and sends real-time notifications to Discord channels via webhooks.

## Features

- **Real-time Monitoring**: Checks Facebook Marketplace every 30 seconds for new phone listings
- **Smart Filtering**: Targets iPhone and Samsung phones under £200 in UK locations
- **Discord Integration**: Rich notifications with phone details, prices, and locations
- **Duplicate Prevention**: Tracks seen listings to avoid spam notifications
- **UK Focused**: Searches major cities like London, Birmingham, Manchester, Glasgow

## Quick Start

### 1. Discord Setup
1. Create a Discord webhook in your server:
   - Right-click your channel → Edit Channel → Integrations → Webhooks
   - Click "New Webhook" and copy the URL

### 2. Railway Deployment
1. Fork/clone this repository
2. Connect to Railway and deploy
3. Add environment variable:
   - `DISCORD_WEBHOOK_URL`: Your Discord webhook URL

### 3. Optional Configuration
Set these environment variables to customize:
- `MONITOR_INTERVAL`: Check frequency in seconds (default: 30)
- `MIN_PRICE`: Minimum price in GBP (default: 0)
- `MAX_PRICE`: Maximum price in GBP (default: 200)

## How It Works

1. **Monitoring Loop**: Bot searches Facebook Marketplace every 30 seconds
2. **Content Filtering**: Finds iPhone and Samsung listings under £200
3. **Location Targeting**: Focuses on UK cities and regions
4. **Duplicate Checking**: Uses hash-based IDs to prevent repeat notifications
5. **Discord Alerts**: Sends formatted notifications with phone details

## Sample Notifications

The bot sends rich Discord embeds containing:
- Phone model and brand
- Price in GBP
- Location in UK
- Condition details
- Storage capacity
- Direct marketplace link

## File Structure

```
├── main.py              # Entry point
├── webhook_bot.py       # Discord webhook integration
├── monitor.py           # Core monitoring logic
├── facebook_connector.py # Marketplace data retrieval
├── web_scraper.py       # Content extraction
├── config.py            # Configuration management
├── utils.py             # Helper functions
├── test_webhook.py      # Webhook testing
├── Procfile             # Railway process definition
├── railway.json         # Railway deployment config
├── runtime.txt          # Python version specification
└── pyproject.toml       # Dependencies
```

## Testing

Run the webhook test to verify Discord integration:
```bash
python test_webhook.py
```

## Railway Deployment

The project includes all necessary Railway configuration:
- **Procfile**: Defines the web process
- **railway.json**: Deployment settings with auto-restart
- **runtime.txt**: Python 3.11 specification
- **pyproject.toml**: All required dependencies

## Monitoring Targets

### iPhone Models
- iPhone 15, 14, 13, 12, 11
- iPhone XS, XR, X, SE
- iPhone Pro, Plus, Mini variants

### Samsung Models
- Galaxy S24, S23, S22, S21
- Galaxy Note series
- Galaxy A series (A54, A34)
- Galaxy Z series

### UK Locations
- London, Greater London
- Birmingham, West Midlands  
- Manchester, Greater Manchester
- Glasgow, Scotland
- Liverpool, Merseyside
- Leeds, West Yorkshire
- Newcastle, Bristol

## Support

The bot automatically restarts on failure and includes comprehensive logging for troubleshooting. Check Railway logs for monitoring status and any issues.

## License

Open source project for personal use monitoring Facebook Marketplace deals.