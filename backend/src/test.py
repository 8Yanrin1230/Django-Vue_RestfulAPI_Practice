import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DcRobot.settings')
import django
django.setup()

from DC.DcRobot import bot

if __name__ == '__main__':
    bot.run('MTIxNjgwMTg4MTQzOTg2MzAzNQ.GQgb05.pQNFZwT8dhc4hqy8hAPARYtPPMeaNUxa_wh4Aw')

