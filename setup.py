"""
Author: Prince Addai Desmond @bubbs.sh
Date: 2024-12-22
Description: turboG or turboGranny is a command-line Python utility that scrapes 
             torrent websites,retrieves .torrent files, and automatically launches 
             a torrent client to begin downloading movies. 
             It is designed use on Linux and Termux environments, offering a simple 
             and fast way to download movies directly from the terminal. :)
"""

#! /usr/bin/env python3

import os
import platform
import subprocess
import sys
import time

bold = "\033[1m"
reset = "\033[0m"



def main():
    art()
    env = detect_env()
    print(env)
    if env == "linux":
        sudo()
    dependencies(env)

def sudo():
    if os.getuid() != 0:
        print(f"This script requires root privileges. Please run it with '{bold}sudo{reset}'.\nUsage: {bold}sudo python3 {sys.argv[0]}{reset}")
        sys.exit(1)



def detect_env():
    if os.path.exists("/data/data/com.termux/files/usr/bin/pkg"):
        return "termux"
    elif platform.system().lower() == "linux":
        return "linux"
    else:
        return "unknown"



def dependencies(env):
    try:
        if env == "termux":
            print(f"\n{bold}Allow storage for Termux{reset}")
            time.sleep(1.5)
            subprocess.run(["termux-setup-storage"], check=True)
            time.sleep(2)
            print(f"{bold}Installing dependencies for Termux{reset}")
            subprocess.run(["apt", "update", "-y"], check=True)
            subprocess.run(["apt", "upgrade", "-y"], check=True)
            subprocess.run(["apt", "install","aria2", "-y"], check=True)
            subprocess.run(["pkg", "update", "-y"], check=True)
            subprocess.run(["apt", "install", "ruby", "python3", "curl","-y"], check=True)
            subprocess.run(["pkg", "install", "libxml2", "libxslt" "-y"]) #these 2 are needed for lxml
            subprocess.run(["gem", "install", "lolcat"], check=True) # For cololized text effect
            subprocess.run(["pip3", "install", "requests", "beautifulsoup4", "cython"], check=True) # cython isfor lxml also
            print(f"\n{bold}lxml may take a while to build.\nPlease don't interrupt.{reset}")
            time.sleep(1)
            command = 'export CFLAGS="-Wno-incompatible-function-pointer-types -Wno-implicit-function-declaration"' # Trust me, I copied this somewhere
            subprocess.run(command, shell=True, check=True)
            subprocess.run('CFLAGS="-O0" pip install lxml', shell=True, check=True) # I got this from reddit, lol
            time.sleep(1)

        elif env == "linux":
            print(f"{bold}Installing dependencies for Linux{reset}")
            subprocess.run(["sudo", "apt", "update", "-y"], check=True)
            subprocess.run(["sudo", "apt", "install","aria2", "-y"], check=True)
            subprocess.run(["sudo", "apt", "install", "python3", "ruby", "lolcat", "curl", "-y"], check=True)
            subprocess.run(["sudo", "apt", "install", "python3-bs4", "python3-requests", "python3-lxml"], check=True)
            #subprocess.run(["pip", "install", "beautifulsoup4", "requests", "lxml"], check=True) # Use this if you prefer pip

        else:
            print("Unsupported OS detected. 🚫\n\n"
            "If you believe this OS should be supported, please raise an issue on GitHub:\n"
            "🔗 https://github.com/bubbs-sh/turboG/issues\n\n"
            "Thank you for helping improve turboG 🙌")
    except:
        pass


def art():
    version = "24.12.22"
    art = r'''
      (\_/)    {0}turboGranny{1} v{2}
     ( •_•)    Downloading dependencies
    / >♥< \    
    '''.format(bold, reset, version)
    subprocess.run(f"echo \"{art}\"", shell=True)
    

if __name__ == "__main__":
    main()