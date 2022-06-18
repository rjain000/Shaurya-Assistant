##############################-PRE DEFINED MODULES-##########################
import webbrowser
import requests
from threading import Thread
##############################-USER DEFINED MODULES-##########################
import listen_n_speak as lns




#note : uncomment lns.speak
def statement(string):
    print(string)
    # lns.speak(string)



def isDomainName(mydomain):
    """checks for domain name and returns None if domain is not available, returns True if domain has https enabled, and returns False if domain has only http"""
    try:
        try:
            r=requests.get(f"https://{mydomain}")
            return True
        except:
            r=requests.get(f"http://{mydomain}")
            return False
    except:
        return None



def web_open(search_content):

    if "https://" in search_content:
        search_content.replace("https://","")

    elif "http://" not in search_content:
        search_content.replace("http://","")
       
    check_https = isDomainName(search_content)

    if check_https == True:
        Thread(target = statement, args = (f"opening {search_content}",)).start()
        webbrowser.open(f"https://{search_content}")
    elif check_https == False:
        Thread(target = statement, args = (f"opening {search_content}",)).start()
        Thread(target = statement, args = (f"{search_content} is not secure. Be carefull",)).start()
        webbrowser.open(f"http://{search_content}")
        
    else:
        Thread(target = statement, args = (f"searching for {search_content}",)).start()
        webbrowser.open(f"https://www.google.com/search?q={search_content}")

