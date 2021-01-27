def menuLiquor():
    menu = 'Welcome to LiquorStore, select an opcion:\n\n[1] See liquor list\n[2] Buy a liquor\n[3] Exit\n'
    return menu

def menuLiquor2():
    menu = '[1] Return to the main menu\n'
    return menu

def menuClient():
    menu = 'Where do you want to connect?\n\n[0] LiquorStore \n[1] Bank\n[2] Exit\n'
    return menu

def menuBank():
    menu = 'Welcome to the Bank!\n\nPlease insert your account number: '
    return menu

def menuBank2(name):
    menu = 'Hello '+name+', what do you want to do?\n\n[0] Check your balance\n[1] Deposit money\n[2] Extract money\n[3] Exit'
    return menu