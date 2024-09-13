from dialogs import home, slave, estate

def setup(dp):
    dp.include_routers(home.dialog, slave.manager, estate.manager, estate.shop, estate.shop_buy)