import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# 1. Flask server to satisfy Render's port binding and keep it awake
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active and compliant.", 200

def run_flask():
    # Render provides the PORT environment variable automatically
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 2. Compliant Telegram Bot Logic
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    STRICT COMPLIANCE RULE: The bot must immediately respond to /start 
    with clear, interactive capabilities on both mobile and desktop.
    """
    user_name = update.effective_user.first_name
    welcome_text = (
        f"Hello {user_name}! Welcome to our official Telegram service.\n\n"
        "Explore our native features below. Everything works seamlessly "
        "directly inside Telegram."
    )
    
    # Inline buttons keep the user inside the native Telegram UI (highly favored by moderators)
    keyboard = [
        [InlineKeyboardButton("🛠️ View Features", callback_data="features")],
        [InlineKeyboardButton("📜 Terms of Service", callback_data="terms")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles interactions to prove the bot is non-vague and deeply interactive."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "features":
        await query.edit_message_text(
            text="✅ **Feature 1:** Native tool tracking.\n✅ **Feature 2:** Instant secure updates.\n\nUse /start to go back.",
            parse_mode="Markdown"
        )
    elif query.data == "terms":
        await query.edit_message_text(
            text="This bot operates under strict compliance with the Telegram Ad Platform Guidelines.",
            parse_mode="Markdown"
        )

def main():
    # Start the Flask web server in a background thread so Render doesn't timeout
    threading.Thread(target=run_flask, daemon=True).start()

    # Start the Telegram Bot Application via polling
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
