
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re, os

BOT_TOKEN = os.getenv("8376473809:AAGh7qmqIrrZNsW6n01woJTNjerju2k7d0c")

async def get_nwm_video_url(tiktok_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    session = requests.Session()
    # Step 1: Load Snaptik and post link
    r = session.get("https://snaptik.app", headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    token = soup.find("input", {"name": "token"})["value"]

    data = {
        "url": tiktok_url,
        "token": token
    }

    res = session.post("https://snaptik.app/abc2.php", headers=headers, data=data)
    soup = BeautifulSoup(res.content, "html.parser")
    links = soup.find_all("a", href=True)

    for a in links:
        if "download" in a["href"] and ".mp4" in a["href"]:
            return a["href"]
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "tiktok.com" not in text:
        await update.message.reply_text("📎 تکایە لینکێکی دروست بنێرە (TikTok only).")
        return

    await update.message.reply_text("⏳ چاوەڕوان بە... دابەزاندنی ڤیدیۆ بەبێ واتەرمارک...")

    try:
        video_url = await get_nwm_video_url(text)
        if video_url:
            await update.message.reply_video(video=video_url, caption="✅ ڤیدیۆکە بەبێ واتەرمارکە 🎉")
        else:
            await update.message.reply_text("❌ نەتوانرا ڤیدیۆیەک بەدەست بهێنرێ.")
    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("🚫 هەڵەیەک ڕوویدا.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 بۆتی TikTok بەبێ واتەرمارک دامەزرابوو!")
app.run_polling()
