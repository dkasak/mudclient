#!/usr/bin/env python

from CompressedTelnet import CompressedTelnet
import thread

def inputter(conn):
    text = ""
    while text != "quit":
        text = raw_input()
        conn.write(text + "\n")
        
# Start as a new thread!
def outputter(conn):
    import time
    try:
        while(True):
            text = conn.read_very_eager()
            if text:
                # Any way to stop print from printing anything
                # after it prints text?
                print text,
                text = None 
            time.sleep(0.1)
    except EOFError:
        print "So this is goodbye..."
        return

host = "discworld.atuin.net"
port = 4242

session = CompressedTelnet()
session.open(host, port)

thid = thread.start_new_thread(outputter, (session,))
inputter(session)    
