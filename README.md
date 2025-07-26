# HYROX Frankfurt Ticket Crawler 🏃‍♂️

> **⚠️ DISCLAIMER: This project is 100% vibe coded.** It was built with pure enthusiasm, minimal planning, and maximum coffee. Use at your own risk and enjoy the chaos! 🎯

A Python script that crawls the [HYROX Frankfurt event page](https://hyrox.com/event/hyrox-frankfurt/) and sends you a Pushover notification when "Ticket sales start soon!" **disappears** from the page (indicating tickets might be available!).

## 🚀 Features

- 🔍 **Smart Crawling**: Monitors HYROX website for ticket availability changes
- 📱 **Pushover Notifications**: Get instant alerts on your phone when tickets drop
- ⚙️ **Environment Variables**: Fully configurable via env vars
- 🤖 **GitHub Actions**: Runs automatically every hour during business hours (8am-7pm Berlin time)
- 🎯 **Reverse Logic**: Notifies when the "coming soon" message disappears
- 🛡️ **Error Handling**: Robust error handling because things break
- 🌍 **Timezone Aware**: Respects Berlin business hours

## 📋 Requirements

- Python 3.11+ (or whatever doesn't break)
- Internet connection
- Pushover account for notifications
- A dream of getting HYROX tickets

## 🔧 Installation

1. Clone this beautiful mess:
```bash
git clone <your-repo>
cd ws-notify-me
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
export PUSHOVER_USER_KEY="your_user_key"
export PUSHOVER_APP_TOKEN="your_app_token"
# Optional overrides:
export CRAWL_URL="https://hyrox.com/event/hyrox-berlin/"
export SEARCH_TERM="Registration opening soon"
```

## 🎮 Usage

### Local Run
```bash
python crawl_hyrox.py
```

### GitHub Actions (Recommended)
1. Add secrets to your repo:
   - `PUSHOVER_USER_KEY`
   - `PUSHOVER_APP_TOKEN`
2. Push to main branch
3. Watch the magic happen every hour! ✨

## 📱 Pushover Setup

1. Create account at [pushover.net](https://pushover.net)
2. Create an application at [pushover.net/apps](https://pushover.net/apps)
3. Grab your User Key and App Token
4. Profit! 💰

## 🔄 How It Works

This script uses **reverse psychology** on the HYROX website:

1. **Normal State**: "Ticket sales start soon!" is present → No notification
2. **ALERT STATE**: Message disappears → 🚨 NOTIFICATION SENT 🚨
3. **You**: Sprint to buy tickets before everyone else!

## 📊 Exit Codes

- `0`: Everything is fine (whether term found or not)
- Non-zero: Something exploded 💥

## 🎯 Example Output

```
🏃‍♂️ HYROX Frankfurt Website Crawler
==================================================
Target URL: https://hyrox.com/event/hyrox-frankfurt/
Searching for: 'Ticket sales start soon!'
Pushover notifications: Enabled
==================================================
🔍 Crawling: https://hyrox.com/event/hyrox-frankfurt/
✅ Successfully fetched the page (Status: 200)
🎯 FOUND: The target term was not found!
📱 Pushover notification sent successfully!

==================================================
🎉 SUCCESS: The target term was not found!
```

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CRAWL_URL` | Frankfurt event page | Which HYROX event to stalk |
| `SEARCH_TERM` | "Ticket sales start soon!" | Text that means "no tickets yet" |
| `PUSHOVER_USER_KEY` | None | Your Pushover user key |
| `PUSHOVER_APP_TOKEN` | None | Your Pushover app token |

## 🕐 GitHub Actions Schedule

Runs every hour from **8am to 7pm Berlin time** because:
- Nobody checks for tickets at 3am (probably)
- Respects Berlin timezone (where HYROX HQ vibes)
- Saves GitHub Actions minutes for other important things

## 🎨 Customization Ideas

Since this is vibe coded, feel free to:
- Add more events to monitor
- Change notification messages
- Add Discord/Slack notifications
- Make it tweet when tickets drop
- Add a database to track price changes
- Whatever your heart desires! 💖

## 🚨 Legal Disclaimer

This is for educational purposes and personal use. Don't use this to:
- Spam websites
- Crash servers
- Buy all the tickets (leave some for others!)
- Anything that would make the HYROX team sad

## 🤝 Contributing

PRs welcome! Since this is vibe coded, just make sure your vibes align with our vibes. ✨

## 📜 License

MIT License because sharing is caring! 🎉

---

*Built with ❤️, ☕, and questionable life choices* 