from bot.booking import Booking
import time
with Booking(teardown=False) as bot:
    bot.land_first_page()
    bot.change_curency()
    time.sleep(5)