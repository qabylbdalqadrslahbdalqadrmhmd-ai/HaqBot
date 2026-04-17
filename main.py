import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from keep_alive import keep_alive

# Start the keep-alive server
keep_alive()

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Configure Gemini AI
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are HaqBot, a highly professional AI legal assistant specializing in Egyptian law. "
        "Provide accurate, professional, and clear legal guidance based on Egyptian statutes. "
        "Always cite the relevant legal articles when possible, and advise the user to consult a licensed lawyer for complex cases. "
        "Respond in the same language as the user's query."
    )
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to HaqBot. I am your professional AI legal assistant for Egyptian law. How can I help you today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("Sorry, an error occurred while processing your request. Please try again later.")

if __name__ == '__main__':
    # Ensure TOKEN is set in your environment variables
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("HaqBot is running...")
    app.run_polling()
