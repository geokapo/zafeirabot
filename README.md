# Zafeirabot 🤖

A personal Telegram AI assistant for crypto analysis and X (Twitter) content strategy.

Built with Python on a Poco M3 running a custom ROM via Termux. Powered by Google Gemini API and CoinGecko.

---

## What it does

- **Crypto prices** — type `bitcoin price` or `monad price` for any coin listed on CoinGecko
- **Crypto analysis** — type `ethereum analysis` or `sol sentiment` for full market data + AI analysis
- **X content** — ask for tweet ideas, hooks, threads, or reply strategies
- **Email analysis** — paste a suspicious email and get SCAM / LEGIT / SUSPICIOUS verdict
- **General AI assistant** — powered by Gemini 2.5 Flash

---

## Requirements

- Python 3.10+
- Termux (Android) or any Linux environment
- Google Gemini API key (Tier 1) — [Get one here](https://aistudio.google.com)
- Telegram Bot token — [Create via @BotFather](https://t.me/BotFather)

---

## Installation

```bash
pip install pyTelegramBotAPI python-dotenv requests
```

---

## Setup

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/zafeirabot.git
cd zafeirabot
```

2. Create your `.env` file:
```bash
cp .env.example .env
nano .env
```

3. Add your keys to `.env`:
```
GEMINI_KEY=your_gemini_api_key_here
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

4. Run:
```bash
python3 bot.py
```

---

## Usage examples

| You type | Bot does |
|----------|----------|
| `bitcoin price` | Live BTC price + 24h change |
| `monad analysis` | Full market data + AI sentiment |
| `kite news` | Market data + BULLISH/BEARISH outlook |
| `write a tweet about Monad` | 3 hook options with different styles |
| `write a thread about AI agents` | Full thread structure |
| `[paste email]` | SCAM / LEGIT / SUSPICIOUS verdict |

---

## Stack

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [Google Gemini API](https://aistudio.google.com) — gemini-2.5-flash
- [CoinGecko API](https://www.coingecko.com/en/api) — free tier with rate limiting
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## Notes

- Never commit your `.env` file
- CoinGecko free API has rate limits — bot handles this automatically with a 2 second delay between requests
- Only one bot instance can run per Telegram token

---

Built by [@Georgia_Kapodistria](https://x.com/tzogirl)
