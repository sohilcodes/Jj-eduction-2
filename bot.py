import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 CONFIG
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 📢 PUBLIC CHANNEL (Bot must be admin)
CHANNEL_USERNAME = "@sohilcodes1"

# 🖼 IMAGE MESSAGE IDs (Upload images in channel in order)
START_MSG_ID = 3834
BEGINNER_MSG_ID = 3835
MARKET_MSG_ID = 3836
RISK_MSG_ID = 3837
STRATEGY_MSG_ID = 3838

bot = telebot.TeleBot(BOT_TOKEN)
users = set()  # For first-time pin logic


# 🎛 MAIN KEYBOARD (2 per row = 3 rows)
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📘 Beginner Guide", "📊 Market Concepts")
    markup.row("⚖️ Risk Management", "🧠 Strategy Basics")
    markup.row("❓ FAQ", "📩 Learning Support")
    return markup


# 📌 Learn More Inline Button
def learn_more_button():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "LEARN MORE",
            url="https://t.me/+zOZC00MmUa40YmQ1"
        )
    )
    return markup


# 🖼 FIXED: Send Image + Separate Keyboard (NO FREEZE BUG)
def send_channel_image(chat_id, msg_id, caption):
    try:
        # Send image from channel
        bot.copy_message(
            chat_id=chat_id,
            from_chat_id=CHANNEL_USERNAME,
            message_id=msg_id,
            caption=caption
        )
    except:
        bot.send_message(chat_id, caption)

    # 🔥 IMPORTANT FIX: Send keyboard separately
    bot.send_message(
        chat_id,
        "📚 Please choose a section from the menu below:",
        reply_markup=main_menu()
    )


# 🚀 START COMMAND (DISCLAIMER → PIN → IMAGE → KEYBOARD)
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    disclaimer = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in loss.
We do not provide financial advice, signals, or guaranteed results.

By continuing, you confirm that you understand and accept this."""

    welcome_text = """Welcome to JJ Learning Assistant Bot 📘

This assistant provides structured educational material
for individuals who want to understand market fundamentals,
risk awareness, and disciplined decision-making principles.

Inside this bot you will find:

• Beginner learning modules
• Market structure explanations
• Risk management fundamentals
• Platform overview (educational)
• Frequently asked questions

This material is provided for educational purposes only.
It does not constitute financial advice.
Market outcomes vary and no results are guaranteed.

Please select a section below to begin."""

    # First-time user → pin disclaimer
    if user_id not in users:
        users.add(user_id)
        sent = bot.send_message(message.chat.id, disclaimer)

        try:
            bot.pin_chat_message(
                chat_id=message.chat.id,
                message_id=sent.message_id,
                disable_notification=True
            )
        except:
            pass
    else:
        bot.send_message(message.chat.id, disclaimer)

    # Send start image + caption + keyboard (fixed)
    send_channel_image(message.chat.id, START_MSG_ID, welcome_text)


# 📘 Beginner Guide
@bot.message_handler(func=lambda message: message.text == "📘 Beginner Guide")
def beginner_guide(message):
    text = """📘 Beginner Guide

This section introduces foundational concepts
for individuals new to financial markets.

Topics covered:

• What trading platforms are
• Basic terminology
• How markets move (conceptual)
• Understanding price charts
• Responsible participation principles

This material is provided for educational purposes only.
It does not constitute financial advice.
Market outcomes vary and no results are guaranteed.

Select a topic below:"""

    send_channel_image(message.chat.id, BEGINNER_MSG_ID, text)


# 📊 Market Concepts
@bot.message_handler(func=lambda message: message.text == "📊 Market Concepts")
def market_concepts(message):
    text = """📊 Market Concepts

Understanding market structure helps improve clarity.

This section explains:

• Trends and ranges
• Support & resistance
• Volatility basics
• Liquidity concepts
• Market psychology

These explanations are conceptual
and do not represent signals or guarantees.

Choose a topic to continue."""

    send_channel_image(message.chat.id, MARKET_MSG_ID, text)


# ⚖️ Risk Management
@bot.message_handler(func=lambda message: message.text == "⚖️ Risk Management")
def risk_management(message):
    text = """⚖️ Risk Management Fundamentals

Risk awareness is essential in any financial activity.

This section explains:

• Position sizing principles
• Exposure control concepts
• Risk-reward balance
• Emotional discipline
• Capital preservation mindset

Responsible decision-making is emphasized.

Educational reference only.
Market outcomes vary.
No guarantees are implied."""

    send_channel_image(message.chat.id, RISK_MSG_ID, text)


# 🧠 Strategy Basics
@bot.message_handler(func=lambda message: message.text == "🧠 Strategy Basics")
def strategy_basics(message):
    text = """🧠 Strategy Basics

Strategies are structured frameworks
used to analyze market behavior.

This section explains:

• Entry & exit theory (conceptual)
• Trend-following logic
• Reversal concepts
• Common beginner mistakes
• Importance of back-testing

No live signals are provided.
This is purely educational discussion."""

    send_channel_image(message.chat.id, STRATEGY_MSG_ID, text)


# ❓ FAQ (NO IMAGE - CLEAN)
@bot.message_handler(func=lambda message: message.text == "❓ FAQ")
def faq(message):
    text = """❓ Frequently Asked Questions

Q: Do you provide trading signals?
A: No. This bot provides educational material only.

Q: Are profits guaranteed?
A: No. Market outcomes vary and no guarantees are implied.

Q: Is this financial advice?
A: No. This content is for informational purposes only.

Q: Should I invest based on this?
A: Always conduct independent research before making financial decisions."""

    bot.send_message(message.chat.id, text, reply_markup=main_menu())


# 📩 Learning Support (INLINE BUTTON)
@bot.message_handler(func=lambda message: message.text == "📩 Learning Support")
def learning_support(message):
    text = """📩 Learning Support

If you would like clarification regarding the educational material
shared inside this bot, you may reach out for further discussion.

Support contact:
@jjtrader_00

Please note:
Support is limited to educational clarification only.
No personal trading advice is provided."""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=learn_more_button()
    )


print("JJ Learning Assistant Bot Running (Fully Fixed Keyboard + No Errors)")
bot.infinity_polling(none_stop=True)
