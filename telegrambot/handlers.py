# # telegrambot/handlers.py
# from asgiref.sync import sync_to_async

# from telegram import Update
# from telegram.ext import ContextTypes, CallbackContext
from .intents import get_intent
# from automation.runner import generate_response, run_method
# from telegrambot.models import Method  # Your model that holds URL + selector config

# async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_message = update.message.text
#     intent = get_intent(user_message)

#     if intent == "greet":
#         await update.message.reply_text("👋 Hello! How can I help you today?")
    
#     elif intent == "show_orders":
#         await update.message.reply_text("📦 You have 2 pending orders. Would you like to view them?")
    
#     elif intent == "help":
#         await update.message.reply_text("🆘 You can ask me about your orders, profile, blog, or type 'generate blog' to auto-create one.")

#     elif intent == "generate_blog":
#         await update.message.reply_text("✍️ Generating a blog now, please hold on...")

#         try:
#             method = await sync_to_async(Method.objects.first)()

#             # method = Method.objects.first()  # Use the first method object for now; customize if needed
#             result = await sync_to_async(run_method)(method)


#             if result["status"] == "success":
#                 await update.message.reply_text(f"✅ Blog created successfully with title:\n*{result['title']}*", parse_mode="Markdown")
#             else:
#                 await update.message.reply_text(f"❌ Failed to generate blog: {result['error']}")

#         except Exception as e:
#             await update.message.reply_text(f"❌ An error occurred: {str(e)}")

#     else:
#         await update.message.reply_text("🤔 Sorry, I didn't understand that. Try asking about your orders, or type 'generate blog'.")

# # Optional: retain this if you still use it separately
# def handle_user_message(update: Update, context: CallbackContext):
#     user_input = update.message.text
#     reply = generate_response(user_input)
#     update.message.reply_text(reply)




# # # telegrambot/handlers.py

# # from telegram import Update
# # from telegram.ext import ContextTypes, CallbackContext
# # from .intents import get_intent
# # from automation.runner import generate_response


# # async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user_message = update.message.text
# #     intent = get_intent(user_message)

# #     if intent == "greet":
# #         await update.message.reply_text("Hello! How can I help you today?")
    
# #     elif intent == "show_orders":
# #         # Example response; you can query your DB here
# #         await update.message.reply_text("You have 2 pending orders. Would you like to view them?")
    
# #     elif intent == "help":
# #         await update.message.reply_text("You can ask me about your orders, profile, or help.")
    
# #     else:
# #         await update.message.reply_text("Sorry, I didn't understand that. Try asking about your orders or type 'help'.")


# # def handle_user_message(update: Update, context: CallbackContext):
# #     user_input = update.message.text
# #     reply = generate_response(user_input)
# #     update.message.reply_text(reply)


from asgiref.sync import sync_to_async
from concurrent.futures import ThreadPoolExecutor
from telegram import Update
from telegram.ext import ContextTypes
from automation.runner import run_method
from telegrambot.models import Method  # Your model that holds URL + selector config

# Create a global ThreadPoolExecutor for handling blocking operations
executor = ThreadPoolExecutor(max_workers=1)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    intent = get_intent(user_message)

    if intent == "greet":
        await update.message.reply_text("👋 Hello! How can I help you today?")
    
    elif intent == "show_orders":
        await update.message.reply_text("📦 You have 2 pending orders. Would you like to view them?")
    
    elif intent == "help":
        await update.message.reply_text("🆘 You can ask me about your orders, profile, blog, or type 'generate blog' to auto-create one.")

    elif intent == "generate_blog":
        await update.message.reply_text("✍️ Generating a blog now, please hold on...")

        try:
            # Ensure method fetching is async-safe
            method = await sync_to_async(Method.objects.first)()

            # Execute the blocking run_method function in a thread
            result = await sync_to_async(executor.submit, thread_pool=True)(run_method, method)

            if result["status"] == "success":
                await update.message.reply_text(f"✅ Blog created successfully with title:\n*{result['title']}*", parse_mode="Markdown")
            else:
                await update.message.reply_text(f"❌ Failed to generate blog: {result['error']}")

        except Exception as e:
            await update.message.reply_text(f"❌ An error occurred: {str(e)}")

    else:
        await update.message.reply_text("🤔 Sorry, I didn't understand that. Try asking about your orders, or type 'generate blog'.")
