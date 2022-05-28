import keyboard

if __name__ == "__main__":
    while True:
        print('begin')
        print(keyboard.is_pressed('ctrl'))
        print('end')