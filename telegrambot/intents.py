# # telegrambot/intents.py

# def get_intent(user_text):
#     """Very basic keyword-based intent detection"""
#     text = user_text.lower()
    
#     if "order" in text:
#         return "show_orders"
#     elif "hello" in text or "hi" in text:
#         return "greet"
#     elif "help" in text:
#         return "help"
#     else:
#         return "unknown"


def get_intent(text):
    text = text.lower()

    if "blog" in text or "write blog" in text:
        return "run_blog"
    elif "appointment" in text or "book" in text:
        return "run_appointment"
    elif "hello" in text or "hi" in text:
        return "greet"
    else:
        return "custom"
