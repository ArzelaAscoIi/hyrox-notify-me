#!/usr/bin/env python3
"""
Daily status ping script for HYROX crawler
"""

import requests
import os
import sys
from datetime import datetime

# Import crawler logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawl_hyrox import crawl_hyrox_website, CRAWL_URL, SEARCH_TERM

# Pushover API Configuration
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"


def send_status_notification(
    user_key: str, app_token: str, message: str, title: str
) -> bool:
    """Send a notification via Pushover API"""
    data = {
        "token": app_token,
        "user": user_key,
        "message": message,
        "title": title,
        "priority": 0,  # Normal priority for status updates
    }

    try:
        response = requests.post(PUSHOVER_API_URL, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == 1:
            print("📱 Status notification sent successfully!")
            return True
        else:
            print(f"❌ Pushover API error: {result.get('errors', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Failed to send status notification: {e}")
        return False


def send_daily_status_ping():
    """Send a daily status notification via Pushover after actually testing the crawler"""

    user_key = os.getenv("PUSHOVER_USER_KEY")
    app_token = os.getenv("PUSHOVER_APP_TOKEN")

    if not user_key or not app_token:
        print("❌ Pushover credentials missing")
        return False

    berlin_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("🧪 Testing crawler functionality...")

    # Actually run the crawler to test functionality
    try:
        # Run without notifications to avoid double-notification
        crawler_result = crawl_hyrox_website(CRAWL_URL, SEARCH_TERM, None, None)
        crawler_status = "✅ WORKING" if crawler_result is not None else "❌ FAILED"

        if crawler_result is True:
            # Term was NOT found (tickets might be available!)
            search_status = (
                f"🚨 ALERT: '{SEARCH_TERM}' NOT found - tickets might be available!"
            )
            emoji = "🚨"
        elif crawler_result is False:
            # Term was found (normal state - no tickets yet)
            search_status = f"🚫 Normal: '{SEARCH_TERM}' still present - no tickets yet"
            emoji = "🤖"
        else:
            # Error occurred
            search_status = "❌ Error occurred during crawling"
            emoji = "⚠️"

    except Exception as e:
        crawler_status = "❌ FAILED"
        search_status = f"❌ Crawler test failed: {str(e)}"
        emoji = "💥"

    message = f"""{emoji} Daily HYROX Crawler Status Report

📅 Date: {berlin_time} (Berlin time)
🔍 Crawler Status: {crawler_status}
🎯 Target: {CRAWL_URL}
📋 Search Term: "{SEARCH_TERM}"

{search_status}

⏰ Last actual test: Just completed
🏃‍♂️ System: Actively monitoring every hour

Keep the faith! 💪"""

    title = f"{emoji} HYROX Crawler Daily Status"

    success = send_status_notification(user_key, app_token, message, title)

    if success:
        print(f"✅ Daily status ping completed successfully")
        print(f"📊 Crawler test result: {crawler_status}")
        print(f"🎯 Search result: {search_status}")

    return success


success = send_daily_status_ping()
if not success:
    exit(1)
