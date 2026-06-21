import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

# 1. 24/7 ሰርቨሩ እንዳይዘጋ የሚያደርግ ነፃ የዌብ ሲስተም (Keep-Alive)
app = Flask('')

@app.route('/')
def home():
    return "King Shield Bot is Online 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

# 2. የቦቱ ዋና የሞደሬሽን ስራዎች
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 እንኳን ደህና መጡ! እኔ ንጉስ ጋሻ (King Shield) የኤአይ ረዳትዎ ነኝ።\n"
        "ይህንን ግሩፕ 24/7 ሙሉ በሙሉ በነፃ እጠብቃለሁ።"
    )

async def monitor_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
        
    text = update.message.text.lower()
    chat_id = update.message.chat_id

    # ማጣሪያ፦ የተከለከሉ እና መጥፎ ቃላትን/ሊንኮችን መለየት
    banned_words = ["ስድብ", "t.me/", "http", "crypto scam", "ቴሌግራም ቻናል"] 
    
    if any(word in text for word in banned_words):
        try:
            # መልዕክቱን ወዲያው ማጥፋት
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            # ማስጠንቀቂያ መላክ
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"⚠️ ተጠቃሚ @{update.message.from_user.username} ህግ ጥሰሃል! መልዕክትህ ጠፍቷል።"
            )
        except Exception as e:
            print(f"Error: {e}")

def main():
    # የቦቱን መለያ ቁጥር ከሰርቨሩ ላይ በነፃ መውሰድ
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable is missing!")
        return

    # ሰርቨሩን 24/7 ማንቃት
    keep_alive()
    
    # ቦቱን ማስጀመር (V20+ ተስማሚ አወቃቀር)
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_messages))
    
    # በሰርቨር ላይ ያለ ችግር እንዲሮጥ
    application.run_polling(close_loop=False)

if __name__ == '__main__':
    main()
