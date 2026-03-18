import requests
import telebot
import os
import time
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY", "YOUR_GEMINI_KEY_HERE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_TOKEN_HERE")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM = (
    "You are a personal AI assistant and expert content strategist for X (Twitter). "
    "The user is a woman with 15 years of experience modding Android devices, active in crypto/Web3 and AI space, building an audience on X.\n\n"
    "IDENTITY & TONE:\n"
    "- Write like a real person, not a marketer\n"
    "- Simple plain English. Short sentences. Direct. Confident.\n"
    "- No corporate speak. No emojis unless asked. No quotes around words for emphasis.\n"
    "- The user is an expert — write at that level\n\n"
    "HOOK RULES:\n"
    "- Never start a tweet with I\n"
    "- Use Pattern Interrupt: say something unexpected or contradictory\n"
    "- Use Information Gap: tease without revealing everything\n"
    "- Use Specific Transformation: before vs after\n"
    "- Use Unspoken Truth: what everyone thinks but nobody says\n"
    "- Best hook types: Unexpected Contradiction, Specific Expensive Mistake, Contrarian Take\n\n"
    "TWEET STRUCTURE:\n"
    "Line 1: Hook stops the scroll, creates curiosity\n"
    "Line 2-3: Body add real value, fact, or insight\n"
    "Last line: Close open loop or real question, never generic\n"
    "Always give exactly 3 options with different hook styles.\n\n"
    "THREAD STRUCTURE:\n"
    "Tweet 1: Hook must work standalone\n"
    "Tweet 2: Backstory or context\n"
    "Tweet 3-5: The meat steps, insights, lessons\n"
    "Tweet 6: Real talk problems you faced\n"
    "Last tweet: CTA with open question, no follow me generic close\n\n"
    "REPLY STRATEGY:\n"
    "- Minimum 8-12 words always\n"
    "- Add a fact, counter-point, or new angle never just agree\n"
    "- End with a real question that sparks conversation\n"
    "- Short sentences, thesis style\n"
    "- Never sound like AI slop\n"
    "- Max 2-3 emojis or none\n\n"
    "CONTENT IDEAS SYSTEM:\n"
    "- 1 great idea shared 10 different ways beats 10 new ideas\n"
    "- Every post must pass the Utility Rule: does it help the reader in some way?\n"
    "- Formats: hot take, tutorial, personal experiment, news commentary, myth-busting\n"
    "- Repurpose articles into threads, threads into single tweets\n\n"
    "EMAIL ANALYSIS:\n"
    "- Verdict: SCAM / LEGIT / SUSPICIOUS\n"
    "- Check for: urgency, prizes, suspicious links, grammar errors, sender mismatch\n"
    "- Explain in 2-3 sentences max\n\n"
    "CRYPTO ANALYSIS:\n"
    "- When given price data and news, provide a clear analysis\n"
    "- Give a sentiment: BULLISH / BEARISH / NEUTRAL with brief reason\n"
    "- Mention key risks and opportunities\n"
    "- Never give financial advice, always add: Not financial advice.\n"
    "- Be direct and concise, no fluff\n\n"
    "CRYPTO KNOWLEDGE:\n"
    "- Bitcoin, Ethereum, Solana: major assets\n"
    "- Monad: high-performance EVM-compatible L1, parallel execution, 10000 TPS\n"
    "- Kite (KITE): AI payment Layer-1 on Avalanche, AI agent transactions\n"
    "- Always factual, never financial advice\n\n"
    "X ALGORITHM KNOWLEDGE (2026):\n"
    "- Grok prioritises human behaviour no burst replies, no bots\n"
    "- Native video gets 3x reach\n"
    "- Threads work best when you already have audience\n"
    "- Single posts better for new accounts to build reach\n"
    "- Best posting time: 8-10am and 7-9pm European time\n"
    "- Quote tweets better than replies for visibility\n"
    "- Images increase completion rate 40%\n"
    "- Ask real questions at end for engagement\n\n"
    "When writing tweets about AI news or Grok updates, frame them from the perspective of a builder and creator, not a spectator."
)

last_request_time = 0


def rate_limit_wait():
    global last_request_time
    now = time.time()
    wait = 2.0 - (now - last_request_time)
    if wait > 0:
        time.sleep(wait)
    last_request_time = time.time()


def search_coin_id(query):
    try:
        rate_limit_wait()
        url = "https://api.coingecko.com/api/v3/search"
        r = requests.get(url, params={"query": query}, timeout=10)
        if r.status_code == 429:
            return None
        r.raise_for_status()
        coins = r.json().get("coins", [])
        if coins:
            return coins[0]["id"]
        return None
    except Exception:
        return None


def get_crypto_price(coin_id):
    rate_limit_wait()
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 429:
            return "Rate limit hit. Wait 30 seconds and try again."
        r.raise_for_status()
        data = r.json()
        if coin_id not in data:
            return None
        price = data[coin_id]["usd"]
        change = data[coin_id].get("usd_24h_change", 0)
        arrow = "🟢" if change >= 0 else "🔴"
        return arrow + " " + coin_id.upper() + ": $" + "{:,.6f}".format(price) + " (" + "{:+.2f}".format(change) + "% 24h)"
    except Exception as e:
        return "Error: " + str(e)


def get_crypto_full_data(coin_id):
    rate_limit_wait()
    try:
        url = "https://api.coingecko.com/api/v3/coins/" + coin_id
        params = {
            "localization": "false",
            "tickers": "false",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false"
        }
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 429:
            return None, "Rate limit hit. Wait 30 seconds and try again."
        r.raise_for_status()
        data = r.json()
        market = data.get("market_data", {})
        price = market.get("current_price", {}).get("usd", 0)
        change_24h = market.get("price_change_percentage_24h", 0) or 0
        change_7d = market.get("price_change_percentage_7d", 0) or 0
        market_cap = market.get("market_cap", {}).get("usd", 0) or 0
        volume = market.get("total_volume", {}).get("usd", 0) or 0
        ath = market.get("ath", {}).get("usd", 0) or 0
        ath_change = market.get("ath_change_percentage", {}).get("usd", 0) or 0
        rank = data.get("market_cap_rank", "N/A")
        desc = data.get("description", {}).get("en", "")
        if desc and len(desc) > 300:
            desc = desc[:300] + "..."
        summary = (
            "Coin: " + data.get("name", coin_id) + " (" + data.get("symbol", "").upper() + ")\n"
            "Rank: #" + str(rank) + "\n"
            "Price: $" + "{:,.6f}".format(price) + "\n"
            "24h: " + "{:+.2f}".format(change_24h) + "%\n"
            "7d: " + "{:+.2f}".format(change_7d) + "%\n"
            "Market Cap: $" + "{:,.0f}".format(market_cap) + "\n"
            "Volume 24h: $" + "{:,.0f}".format(volume) + "\n"
            "ATH: $" + "{:,.6f}".format(ath) + " (" + "{:+.1f}".format(ath_change) + "% from ATH)\n"
        )
        if desc:
            summary += "About: " + desc + "\n"
        return summary, None
    except Exception as e:
        return None, "Error: " + str(e)


def ask_gemini(user_text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + GEMINI_KEY
    payload = {
        "contents": [{
            "parts": [{"text": SYSTEM + "\n\nUser: " + user_text}]
        }]
    }
    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        response_data = r.json()
        if "candidates" not in response_data:
            return "Gemini error: " + str(response_data)
        return response_data["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.Timeout:
        return "Request timed out. Try again."
    except requests.exceptions.RequestException as e:
        return "Network error: " + str(e)
    except (KeyError, IndexError):
        return "Unexpected response format from Gemini."


def extract_coin_query(text):
    stop_words = {"price", "analysis", "analyze", "news", "sentiment", "prediction",
                  "outlook", "τιμη", "τιμή", "αναλυση", "ανάλυση", "ειδησεις",
                  "ειδήσεις", "the", "a", "an", "of", "for", "me", "give", "show",
                  "what", "is", "how", "much", "προβλεψη", "πρόβλεψη"}
    words = text.lower().split()
    candidates = [w for w in words if w not in stop_words and len(w) > 1]
    return candidates[0] if candidates else None


@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.lower().strip()

    analysis_keywords = ["analysis", "analyze", "ανάλυση", "αναλυση", "sentiment",
                         "prediction", "outlook", "news", "ειδήσεις", "ειδησεις", "πρόβλεψη", "προβλεψη"]
    price_keywords = ["price", "τιμη", "τιμή"]

    is_price = any(k in text for k in price_keywords)
    is_analysis = any(k in text for k in analysis_keywords)

    if is_price or is_analysis:
        coin_query = extract_coin_query(text)
        if not coin_query:
            bot.reply_to(message, ask_gemini(message.text))
            return

        bot.reply_to(message, "Searching for " + coin_query.upper() + "...")
        coin_id = search_coin_id(coin_query)

        if not coin_id:
            bot.reply_to(message, "Could not find " + coin_query.upper() + " on CoinGecko.")
            return

        if is_analysis:
            full_data, error = get_crypto_full_data(coin_id)
            if error:
                bot.reply_to(message, error)
                return
            prompt = (
                "Analyze this crypto asset and give:\n"
                "1. Quick price summary\n"
                "2. Sentiment: BULLISH / BEARISH / NEUTRAL with reason\n"
                "3. Key risks\n"
                "4. Key opportunities\n"
                "5. Short-term outlook\n\n"
                + full_data +
                "\nBe direct and concise. Not financial advice."
            )
            analysis = ask_gemini(prompt)
            bot.reply_to(message, analysis)
        else:
            result = get_crypto_price(coin_id)
            if result:
                bot.reply_to(message, result)
            else:
                bot.reply_to(message, "Could not fetch price for " + coin_query.upper())
        return

    reply = ask_gemini(message.text)
    bot.reply_to(message, reply)


print("Bot running...")
bot.infinity_polling(timeout=30, long_polling_timeout=30)