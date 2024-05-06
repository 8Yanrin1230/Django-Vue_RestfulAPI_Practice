import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DcRobot.settings')
import django
django.setup()

from DC.DcRobot import bot

if __name__ == '__main__':
    bot.run('MTIxNjgwMTg4MTQzOTg2MzAzNQ.GrSmt1.TBI2C-fKE35IEhU5SyVQ3Ibn_2PcWs2SSbHZR0')
