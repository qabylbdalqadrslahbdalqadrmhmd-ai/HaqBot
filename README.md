
import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from keep_alive import keep_alive

keep_alive()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are HaqBot, a professional AI legal assistant specializing in Egyptian law. "
        "Provide accurate, professional, and clear legal guidance based on Egyptian statutes. "
        "Always cite relevant legal articles when possible, and advise users to consult a licensed lawyer for complex matters. "
        "Maintain a formal and helpful tone."
    )
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to HaqBot. How can I assist you with Egyptian law today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred while processing your query. Please try again later.")

if __name__ == '__main__':
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("HaqBot is running...")
    app.run_polling()
