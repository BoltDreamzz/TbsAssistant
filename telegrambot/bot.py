import os
from asgiref.sync import sync_to_async

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from automation.runner import run_method
from .models import Method
from .intents import get_intent

from telegram.ext import ConversationHandler

(
    GET_NAME,
    GET_EMAIL,
    GET_PHONE,
    GET_DATE,
    GET_TIME,
    CONFIRM_BOOKING,
) = range(6)


TELEGRAM_TOKEN = '7790390426:AAGP6LcmbqMDTret1d3lJEn45sMThSvTXQM'



# ----- Sync to Async Wrappers -----

@sync_to_async
def get_method_by_keyword(keyword):
    return Method.objects.filter(name__icontains=keyword).first()


# ----- Start Command -----

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Fill Blog Form", callback_data="run_blog")],
        [InlineKeyboardButton("Book Appointment", callback_data="run_appointment")],
        [InlineKeyboardButton("Custom Prompt", callback_data="custom_prompt")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to Tbs AutoBot. How can I help you?", reply_markup=reply_markup
    )


# ----- Callback Query Handler -----

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "run_blog":
        method = await get_method_by_keyword("blog")
        if method:
            result = await run_method(method)
            await query.edit_message_text(f"✅ Blog Form Executed.\nStatus: {result}")
        else:
            await query.edit_message_text("❌ No 'blog' method found.")

    elif query.data == "run_appointment":
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Let's get started with your booking."
        )
        return GET_NAME  # triggers the conversation flow

    elif query.data == "custom_prompt":
        await query.edit_message_text("✍️ Send your custom command or website prompt:")


# ----- Callback Query Handler with Loading & Error Handling -----

# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     if query.data in ["run_blog", "run_appointment"]:
#         action = "Blog Form" if query.data == "run_blog" else "Appointment"
#         loading_msg = await query.edit_message_text(f"⏳ Processing {action}...")

#         try:
#             keyword = "blog" if query.data == "run_blog" else "appointment"
#             method = await get_method_by_keyword(keyword)

#             if method:
#                 result = run_method(method)

#                 await loading_msg.edit_text(f"✅ {action} Executed.\nStatus: {result}")
#             else:
#                 await loading_msg.edit_text(f"❌ No '{keyword}' method found.")
#         except Exception as e:
#             await loading_msg.edit_text(f"⚠️ An error occurred: {str(e)}")

#     elif query.data == "custom_prompt":
#         await query.edit_message_text("✍️ Send your custom command or website prompt:")


# ----- Text Message Handler -----

# ----- Text Message Handler with Loading & Error Handling -----

async def custom_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    intent = get_intent(text)

    if intent == "greet":
        await update.message.reply_text("👋 Hello! How can I assist you today?")

    elif intent in ["run_blog", "run_appointment"]:
        action = "Blog" if intent == "run_blog" else "Appointment"
        loading_msg = await update.message.reply_text(f"⏳ Processing {action}...")

        try:
            keyword = "blog" if intent == "run_blog" else "appointment"
            method = await get_method_by_keyword(keyword)

            if method:
                result = run_method(method)

                if result["status"] == "success":
                    await loading_msg.edit_text(f"📝 {action} Created: {result['title']}")
                    with open(result["screenshot"], "rb") as img:
                        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)
                else:
                    await loading_msg.edit_text(f"❌ Failed: {result['error']}")
            else:
                await loading_msg.edit_text(f"❌ No '{keyword}' method found.")
        except Exception as e:
            await loading_msg.edit_text(f"⚠️ An error occurred: {str(e)}")

    else:
        await update.message.reply_text(
            f"You said: {text}\n\n🧠 I didn't fully understand that, but I'm learning!"
        )




# --- In your `bot.py` or a separate file for database operations ---
from asgiref.sync import sync_to_async
from bookings.models import Appointment, Booking, Service
from datetime import datetime

# Fetch the available service (could be pre-populated or prompted by bot)
@sync_to_async
def get_service_by_name(name):
    return Service.objects.filter(name__icontains=name).first()


# Step 1: Get Name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter your *full name*:", parse_mode="Markdown")
    return GET_EMAIL

# Step 2: Get Email
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Enter your *email address*:", parse_mode="Markdown")
    return GET_PHONE

# Step 3: Get Phone
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("Enter your *phone number*:", parse_mode="Markdown")
    return GET_DATE

# Step 4: Get Date
async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("What *date* would you like? (YYYY-MM-DD)", parse_mode="Markdown")
    return GET_TIME

# Step 5: Get Time
async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("What *time* would you like? (HH:MM)", parse_mode="Markdown")
    return CONFIRM_BOOKING

# Step 6: Save Booking
@sync_to_async
def save_booking(user_data):
    from bookings.models import Booking, Service  # import inside to avoid circular imports
    service = Service.objects.first()  # or use a specific one

    return Booking.objects.create(
        name=user_data["name"],
        email=user_data["email"],
        phone=user_data["phone"],
        service=service,
        date=user_data["date"],
        time=user_data["time"]
    )

async def confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text

    try:
        booking = await save_booking(context.user_data)
        await update.message.reply_text(
            f"✅ Booking confirmed for *{booking.date}* at *{booking.time}*\nWe'll reach out soon!",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Something went wrong: {str(e)}")

    return ConversationHandler.END



# Create a booking record
@sync_to_async
def create_booking(name, email, phone, service, date, time):
    return Booking.objects.create(
        name=name,
        email=email,
        phone=phone,
        service=service,
        date=date,
        time=time
    )

# Create an appointment record
@sync_to_async
def create_appointment(user, service, date, time):
    return Appointment.objects.create(
        user=user,
        service=service,
        date=date,
        time=time
    )


# ----- Run the Bot -----

def run_telegram_bot():
    print("🤖 Starting Telegram Bot...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, custom_text))

    booking_convo = ConversationHandler(
    entry_points=[CallbackQueryHandler(get_name, pattern="^run_appointment$")],
    states={
        GET_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        GET_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        GET_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
        GET_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        CONFIRM_BOOKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_booking)],
    },
    fallbacks=[],
    
)


    app.add_handler(booking_convo)

    app.run_polling()
