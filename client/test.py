from client import Client
import time
from threading import Thread

c1 = Client("Moua")
c2 = Client("Devin")



def update_messages():
    msgs = []
    run = True
    while run:
        time.sleep(0.1)     # update every 0.1 seconds
        new_messages = c1.get_messages()    # get new message
        msgs.extend(new_messages)           # add to local list message
        for msg in new_messages:            # display new messages
            print(msg)
            if msg == "{quit}":
                run = False
                break

Thread(target=update_messages).start()

c1.send_message("hello")
time.sleep(5)
c2.send_message("how's going")
time.sleep(5)
c1.send_message("I'm doing all right, and you?")
time.sleep(5)
c2.send_message("It's a boring day...")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()