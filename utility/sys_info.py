##########################-PRE-DEFINED FUNCTIONS-################
import psutil
import time
import pyautogui
import network
import sqlite3




def check_terminate():
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()
    cur_obj.execute("select status from device_control where device_name = 'terminate'; ")
    value = cur_obj.fetchone()
    value = value[0]
    cur_obj.close()
    instance.commit()
    instance.close()
    return value

def battery_info(labels, imgs):
    """regular checks for the battery percentage"""

    #label[0] image 100x80 
    #label[1] percent image 100x20

    #charging icons
    # imgs[0][0]        -> 10%
    # imgs[0][1]        -> 25%
    # imgs[0][2]        -> 50%
    # imgs[0][3]        -> 75%
    # imgs[0][4]        -> 100%

    #not charging icons
    # imgs[1][0]        -> 10%
    # imgs[1][1]        -> 25%
    # imgs[1][2]        -> 50%
    # imgs[1][3]        -> 75%
    # imgs[1][4]        -> 100%
    status_return = True
    while status_return:
        try:
            # returns associative tuple
            battery = psutil.sensors_battery()

            if battery.power_plugged:
                if battery.percent==100:
                    labels[0].config(image= imgs[0][4])
                    labels[1].config(foreground="white")
                    labels[1].config(text="Full")
                    time.sleep(1)             
                    
                elif battery.percent<100 and battery.percent>80:
                    labels[0].config(image= imgs[0][3])
                    labels[1].config(foreground="#6dcc00")
                                                
                elif battery.percent<=80 and battery.percent>50:
                    labels[0].config(image= imgs[0][2])
                    labels[1].config(foreground="#dbdb01")
                    
                elif battery.percent<=50 and battery.percent>20:
                    labels[0].config(image= imgs[0][1])
                    labels[1].config(foreground="#ff9f00")               
                    
                else:
                    labels[0].config(image= imgs[0][0])
                    labels[1].config(foreground="white")                
                    
            else:
                if battery.percent==100:
                    labels[0].config(image= imgs[1][4])
                    labels[1].config(foreground="white")               
                    
                elif battery.percent<100 and battery.percent>80:
                    labels[0].config(image= imgs[1][3])
                    labels[1].config(foreground="#6dcc00")
                                                
                elif battery.percent<=80 and battery.percent>50:
                    labels[0].config(image= imgs[1][2])
                    labels[1].config(foreground="#dbdb01")              
                                
                    
                elif battery.percent<=50 and battery.percent>20:
                    labels[0].config(image= imgs[1][1])
                    labels[1].config(foreground="#ff9f00")               
                    
                else:
                    labels[0].config(image= imgs[1][0])
                    labels[1].config(foreground="white")

            labels[1].config(text= " "+str(battery.percent)+"%")
        except:
            pass
        finally:
            if check_terminate() == "on":
                print('battery_info Function Ends ')
                status_return = False
                return ""  
                
        time.sleep(2)
        

def system_volume_control(up= None, down= None, mute= None, unmute= None):
    if up == True:
        print("volume up")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        
        
    elif down == True:
        print("volume down")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
    
    elif mute == True:
        print("volume mute")
        pyautogui.press("volumeup")
        pyautogui.press("volumemute")

    elif unmute == True:
        print("volume unmute")
        pyautogui.press("volumeup")

    else:
        print("nothing done for volume control")
        pass
    

def system_config(cpu, memory, _network):
    
    last_received = psutil.net_io_counters().bytes_recv
    last_send = psutil.net_io_counters().bytes_sent
    status_return = True
    while status_return:
        try:
            cpu_usage = psutil.cpu_percent(0.5)
            
            memory_usage = psutil.virtual_memory()[2]
            
            bytes_received = psutil.net_io_counters().bytes_recv
            bytes_send = psutil.net_io_counters().bytes_sent

            new_received = (bytes_received - last_received) /1024 / 1024
            new_send = (bytes_send - last_send) / 1024 / 1024

            total_usage = new_received + new_send

            last_received = psutil.net_io_counters().bytes_recv
            last_send = psutil.net_io_counters().bytes_sent

            cpu['text'] = "CPU: "+str(int(cpu_usage))+"%"
            memory['text'] = "Memory: "+str(int(memory_usage))+"%"
            _network['text'] = f"Network: {total_usage:.2f}MB"
        except:
            pass
        finally:
            if check_terminate() == "on":
                print('system_config Functions Ends')
                status_return = False
                return ""
            time.sleep(1)


def network_check(label, imgs, label_info):
    #imgs[0]    ----> connected
    #imgs[1]    ----> not connected
    status_return = True
    while status_return:
        try:
            if network.isConnected() == True:
                label['image'] = imgs[0]
                label_info['text'] = "Connected"

            else:
                label['image'] = imgs[1]
                label_info['text'] = "No Internet"
        except:
            pass
        finally:
            if check_terminate() == "on":
                print('network_check functions ends')
                status_return = False
                return ""
            time.sleep(2)


def check_disk_space(label=None, info_label=None):
	import wmi
	c = wmi.WMI()  
	my_system_1 = c.Win32_LogicalDisk()[0]
	info = ["Total Disk Space: " + str(round(int(my_system_1.Size)/(1024**3),2)) + " GB"]
	return info
