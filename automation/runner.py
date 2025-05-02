# automation/runner.py
# automation/runner.py

from playwright.sync_api import sync_playwright
from telegrambot.openrouter_client import generate_openrouter_response
from blog.models import Blog
from asgiref.sync import sync_to_async  # Add this import


@sync_to_async
def save_blog_to_db(title, body):
    Blog.objects.create(title=title, content=body)


async def generate_blog_content():
    prompt = (
        "You are an intelligent and helpful assistant. "
        "Please generate a catchy blog title and a short 3-paragraph blog post "
        "about a trending topic in Hair Diseases to urge clients to want to book a session with us to resolve their hair issues."
    )

    result = generate_openrouter_response(prompt)

    try:
        parts = result.split("\n", 1)
        title = parts[0].strip()
        body = parts[1].strip() if len(parts) > 1 else ""

        # Save asynchronously
        await save_blog_to_db(title, body)

        return title, body

    except Exception as e:
        raise Exception(f"❌ Error parsing or saving blog: {str(e)}")


async def run_method(method):
    try:
        title, body = await generate_blog_content()

        def automate_browser():
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                page.goto(method.url)

                selectors = method.selector or {
                    "title": "#title",
                    "content": "#content",
                    "submit": "#submit"
                }

                page.fill(selectors["title"], title)
                page.fill(selectors["content"], body)
                page.click(selectors["submit"])

                page.wait_for_load_state("networkidle")
                screenshot_path = "blog_success.png"
                page.screenshot(path=screenshot_path)

                context.close()
                browser.close()

                return {
                    "status": "success",
                    "screenshot": screenshot_path,
                    "title": title
                }

        from asyncio import to_thread
        return await to_thread(automate_browser)

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }


def generate_response(user_input):
    return generate_openrouter_response(user_input)




# # automation/runner.py

# from playwright.sync_api import sync_playwright
# from .generator import generate_blog_content
# from telegrambot.openrouter_client import generate_openrouter_response


# def run_method(method):
#     try:
#         title, body = generate_blog_content()

#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=True)
#             context = browser.new_context()
#             page = context.new_page()

#             page.goto(method.url)

#             # Simulated selectors from method.selector (if set)
#             selectors = method.selector or {
#                 "title": "#title",  # Example input field selectors
#                 "content": "#content",
#                 "submit": "#submit"
#             }

#             page.fill(selectors["title"], title)
#             page.fill(selectors["content"], body)
#             page.click(selectors["submit"])

#             page.wait_for_load_state("networkidle")
#             screenshot_path = "blog_success.png"
#             page.screenshot(path=screenshot_path)

#             context.close()
#             browser.close()

#             return {
#                 "status": "success",
#                 "screenshot": screenshot_path,
#                 "title": title
#             }

#     except Exception as e:
#         return {
#             "status": "failed",
#             "error": str(e)
#         }


# # automation/runner.py
# from telegrambot.openrouter_client import generate_openrouter_response

# def generate_response(user_input):
#     return generate_openrouter_response(user_input)

