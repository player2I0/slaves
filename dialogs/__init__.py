from dialogs import home, slave

def setup(dp):
    dp.include_routers(home.dialog, slave.manager)