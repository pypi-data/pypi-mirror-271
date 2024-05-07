import pyotp

def func1():
    print('func1')


def func2(key):
    totp = pyotp.TOTP(key)
    print(totp.now())