from django.core.management.base import BaseCommand
from telegrambot.bot import run_telegram_bot

class Command(BaseCommand):
    help = "Start the Telegram bot"

    def handle(self, *args, **kwargs):
        self.stdout.write("🤖 Starting Telegram Bot...")
        run_telegram_bot()
