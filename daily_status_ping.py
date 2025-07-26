#!/usr/bin/env python3
"""
Daily status ping script for HYROX crawler
"""

import requests
import os
from datetime import datetime


def send_daily_status_ping():
    """Send a daily status notification via Pushover"""

    user_key = os.getenv("PUSHOVER_USER_KEY")
    app_token = os.getenv("PUSHOVER_APP_TOKEN")

    if not user_key or not app_token:
        print("❌ Pushover credentials missing")
        return False

    berlin_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    message = f"""🤖 Daily HYROX Crawler Status Report

📅 Date: {berlin_time} (Berlin time)
🔍 Status: Still monitoring for tickets!
🎯 Target: HYROX Frankfurt 
📋 Current search: "Ticket sales start soon!"

✅ System is healthy and checking every hour
⏰ Last checked: Just now
🚫 No tickets available yet - still waiting for the magic moment!

Keep the faith! 🏃‍♂️💪"""

    data = {
        "token": app_token,
        "user": user_key,
        "message": message,
        "title": "🏃‍♂️ HYROX Crawler Daily Status",
        "priority": 0,  # Normal priority for status updates
    }

    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json", data=data, timeout=10
        )
        response.raise_for_status()
        result = response.json()

        if result.get("status") == 1:
            print("📱 Daily status notification sent successfully!")
            return True
        else:
            print(f"❌ Pushover API error: {result.get('errors', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Failed to send status notification: {e}")
        return False


success = send_daily_status_ping()
if not success:
    exit(1)
