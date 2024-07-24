from bot.booking import Booking
with Booking(teardown=False) as bot:
    bot.land_first_page()
    bot.change_curency()
    bot.select_place_to_go('Ahemdabad')
    bot.select_dates('2024-07-31', '2024-08-10')
    bot.select_guests(count=5)
    bot.click_search()
    bot.apply_filteration()
