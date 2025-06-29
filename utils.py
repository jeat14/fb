"""
Utility functions for the Discord bot
"""
import re
from typing import Dict

def extract_phone_info(title: str, description: str = "") -> Dict[str, str]:
    """
    Extract phone information from listing title and description
    
    Args:
        title: Listing title
        description: Listing description
        
    Returns:
        Dict containing extracted phone information
    """
    combined_text = f"{title} {description}".lower()
    info = {}
    
    # Extract brand
    if "iphone" in combined_text:
        info["brand"] = "iPhone"
        # Extract iPhone model
        iphone_models = ["15", "14", "13", "12", "11", "xs", "xr", "x", "se"]
        for model in iphone_models:
            if f"iphone {model}" in combined_text or f"iphone{model}" in combined_text:
                info["model"] = model.upper()
                break
    elif "samsung" in combined_text or "galaxy" in combined_text:
        info["brand"] = "Samsung"
        # Extract Samsung model
        samsung_models = ["s24", "s23", "s22", "s21", "note", "a54", "a34"]
        for model in samsung_models:
            if model in combined_text:
                info["model"] = model.upper()
                break
    
    # Extract storage capacity
    storage_match = re.search(r'(\d+)(gb|tb)', combined_text)
    if storage_match:
        capacity = storage_match.group(1)
        unit = storage_match.group(2).upper()
        info["storage"] = f"{capacity}{unit}"
    
    # Extract condition
    conditions = ["new", "excellent", "good", "fair", "poor", "refurbished", "unlocked"]
    for condition in conditions:
        if condition in combined_text:
            info["condition"] = condition.title()
            break
    
    return info

def format_price(price_str: str) -> str:
    """
    Format price string to UK pounds format
    
    Args:
        price_str: Raw price string
        
    Returns:
        Formatted price string in £
    """
    # Extract numeric value
    price_match = re.search(r'(\d+)', price_str)
    if price_match:
        price = price_match.group(1)
        return f"£{price}"
    return price_str

def create_webhook_embed(listing: Dict) -> Dict:
    """
    Create a Discord webhook embed for a phone listing
    
    Args:
        listing: Dictionary containing listing information
        
    Returns:
        Dictionary containing webhook embed data
    """
    title = listing.get("title", "Unknown Phone")
    price = listing.get("price", "Price not available")
    location = listing.get("location", "UK")
    description = listing.get("description", "")
    url = listing.get("url", "")
    
    # Extract phone information
    phone_info = extract_phone_info(title, description)
    
    # Create embed fields
    fields = []
    
    if phone_info.get("brand"):
        fields.append({
            "name": "📱 Brand",
            "value": phone_info["brand"],
            "inline": True
        })
    
    if phone_info.get("model"):
        fields.append({
            "name": "📋 Model",
            "value": phone_info["model"],
            "inline": True
        })
    
    if phone_info.get("storage"):
        fields.append({
            "name": "💾 Storage",
            "value": phone_info["storage"],
            "inline": True
        })
    
    if phone_info.get("condition"):
        fields.append({
            "name": "✨ Condition",
            "value": phone_info["condition"],
            "inline": True
        })
    
    fields.append({
        "name": "📍 Location",
        "value": location,
        "inline": True
    })
    
    # Determine embed color based on price
    price_num_match = re.search(r'(\d+)', price)
    color = 0x00ff00  # Green for good deals
    if price_num_match:
        price_num = int(price_num_match.group(1))
        if price_num <= 100:
            color = 0x00ff00  # Green for under £100
        elif price_num <= 150:
            color = 0xffff00  # Yellow for under £150
        else:
            color = 0xff6600  # Orange for higher prices
    
    embed_data = {
        "title": f"🔥 {title}",
        "description": f"**{price}**\n\n{description[:200]}{'...' if len(description) > 200 else ''}",
        "color": color,
        "fields": fields,
        "footer": {
            "text": "Facebook Marketplace UK • Phone Monitor Bot"
        },
        "timestamp": listing.get("timestamp", "")
    }
    
    # Add URL if available
    if url:
        embed_data["url"] = url
    
    return embed_data

def is_valid_phone_listing(listing: Dict) -> bool:
    """
    Check if a listing is a valid phone listing
    
    Args:
        listing: Dictionary containing listing information
        
    Returns:
        Boolean indicating if listing is valid
    """
    if not listing:
        return False
    
    title = listing.get("title", "").lower()
    description = listing.get("description", "").lower()
    combined_text = f"{title} {description}"
    
    # Must contain phone-related terms
    phone_terms = ["iphone", "samsung", "galaxy", "phone", "smartphone"]
    has_phone_term = any(term in combined_text for term in phone_terms)
    
    if not has_phone_term:
        return False
    
    # Must have a price
    price = listing.get("price", "")
    if not price or price == "Price not available":
        return False
    
    # Must have a title
    if not listing.get("title"):
        return False
    
    return True