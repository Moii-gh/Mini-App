import time 

def running_text(text):
    for i in range(len(text) + 1):
        print('\r' + text, end = '')
        time.sleep(0.2)
        text = text[1:] + text[0]

running_text("hello world")