#!/usr/bin/env python3
"""
Simple web crawler to check for "Ticket sales start soon!" on HYROX Frankfurt website
"""

import os
import requests
from bs4 import BeautifulSoup
import sys
from typing import Dict, List, Optional

# Pushover API Configuration
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_NOTIFICATION_TITLE = "HYROX Tickets Available!"
PUSHOVER_DEFAULT_TITLE = "HYROX Crawler Alert"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


# We crawl until we don't find a term any more
# Usually thats the indicator that the website was updated
CRAWL_URL: str = os.getenv("CRAWL_URL", "https://hyrox.com/event/hyrox-frankfurt/")
SEARCH_TERM: str = os.getenv("SEARCH_TERM", "Ticket sales start soon!")
PUSHOVER_USER_KEY: str | None = os.getenv("PUSHOVER_USER_KEY", None)
PUSHOVER_APP_TOKEN: str | None = os.getenv("PUSHOVER_APP_TOKEN", None)

if not all([PUSHOVER_USER_KEY, PUSHOVER_APP_TOKEN]):
    print("❌ Pushover credentials not provided - skipping notification")
    sys.exit(0)


def send_pushover_notification(
    user_key: str, app_token: str, message: str, title: str = PUSHOVER_DEFAULT_TITLE
) -> bool:
    """
    Send a push notification via Pushover API

    Args:
        user_key (str): Pushover user key
        app_token (str): Pushover application token
        message (str): The message to send
        title (str): The notification title

    Returns:
        bool: True if notification sent successfully, False otherwise
    """
    try:
        data: Dict[str, str] = {
            "token": app_token,
            "user": user_key,
            "message": message,
            "title": title,
        }

        response: requests.Response = requests.post(
            PUSHOVER_API_URL, data=data, timeout=10
        )
        response.raise_for_status()

        result: Dict = response.json()
        if result.get("status") == 1:
            print("📱 Pushover notification sent successfully!")
            return True
        else:
            print(f"❌ Pushover API error: {result.get('errors', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"❌ Failed to send Pushover notification: {e}")
        return False


def crawl_hyrox_website(
    url: str,
    search_term: str,
    user_key: Optional[str] = None,
    app_token: Optional[str] = None,
) -> bool:
    """
    Crawl the HYROX website and search for the specified term

    Args:
        url (str): The URL to crawl
        search_term (str): The term to search for
        user_key (str, optional): Pushover user key for notifications
        app_token (str, optional): Pushover app token for notifications

    Returns:
        bool: True if term found, False otherwise
    """

    try:
        print(f"🔍 Crawling: {url}")

        headers: Dict[str, str] = {"User-Agent": USER_AGENT}

        response: requests.Response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        print(f"✅ Successfully fetched the page (Status: {response.status_code})")

        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        # Get all text content from the page
        page_text: str = soup.get_text()

        if search_term.lower() in page_text.lower():
            print(f"🎯 FOUND: '{search_term}' was found on the page!")

            # Try to find the exact context where the term appears
            lines: List[str] = page_text.split("\n")
            context_line: str = ""
            for i, line in enumerate(lines):
                if search_term.lower() in line.lower():
                    context_line = line.strip()
                    print(f"📍 Context (line {i + 1}): {context_line}")
                    break

            # Send Pushover notification if credentials are provided
            if user_key and app_token:
                notification_message: str = f"🎉 HYROX Frankfurt tickets update!\n\nFound: '{search_term}'\nURL: {url}\nContext: {context_line}"
                send_pushover_notification(
                    user_key,
                    app_token,
                    notification_message,
                    PUSHOVER_NOTIFICATION_TITLE,
                )
            else:
                print("📱 Pushover credentials not provided - skipping notification")

            return True
        else:
            print(f"❌ STILL PRESENT: '{search_term}' was found on the page.")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching the website: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main() -> None:
    """Main function to run the crawler"""

    print("🏃‍♂️ HYROX Frankfurt Website Crawler")
    print("=" * 50)
    print(f"Target URL: {CRAWL_URL}")
    print(f"Searching for: '{SEARCH_TERM}'")
    print(
        f"Pushover notifications: {'Enabled' if PUSHOVER_USER_KEY and PUSHOVER_APP_TOKEN else 'Disabled (missing credentials)'}"
    )
    print("=" * 50)

    # Perform the crawl
    found: bool = crawl_hyrox_website(
        CRAWL_URL, SEARCH_TERM, PUSHOVER_USER_KEY, PUSHOVER_APP_TOKEN
    )

    print("\n" + "=" * 50)
    if found:
        print("🎉 SUCCESS: The target term was not found!")
        sys.exit(0)
    else:
        print("😞 RESULT: The target term was found.")
        sys.exit(0)


main()
