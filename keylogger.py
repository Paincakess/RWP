import pynput.keyboard as k

def key_press(key):
    print (key)

listen_keyboard = k.Listener(on_press=key_press)
with listen_keyboard:
    listen_keyboard.join()