############################# PRE-DEFINED MODULES ####################################
import socket

############################# PRE-DEFINED MODULES ####################################

############################# FUNCTIONS ####################################

def myIP():
    """Returns IP Address of your device"""
    IP_ADDRESS = socket.gethostbyname(socket.gethostname())
    return IP_ADDRESS

def isConnected():
    """Returns True if Computer is connected to internet else return False"""
    ip = myIP()
    if ip == "127.0.0.1":
        return False
    else:
        return True
