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
            print(f"{bold}Installing dependencies for Termux{reset}")
            subprocess.run(["apt", "update", "-y"], check=True)
            subprocess.run(["apt", "install","aria2", "-y"], check=True)
            subprocess.run(["pkg", "update", "-y"], check=True)
            subprocess.run(["pkg", "install", "ruby", "python3", "curl","-y"], check=True)
            subprocess.run(["gem", "install", "lolcat"], check=True)
            subprocess.run(["pip3", "install", "requests", "beautifulsoup4"], check=True)
            print(f"\n{bold}lxml may take a while to build.\nPlease don't interrupt.{reset}")
            time.sleep(1)
            command = 'export CFLAGS="-Wno-incompatible-function-pointer-types -Wno-implicit-function-declaration" && echo $CFLAGS'
            subprocess.run(command, shell=True, check=True)
            subprocess.run(["pip3", "install", "lxml"], check=True)
        
            # subprocess.run(['CFLAGS="-O0"', "pip", "install", "lxml"], check=True)
            time.sleep(1)
            print(f"\n{bold}Setup storage for termux{reset}")
            time.sleep(1)
            subprocess.run(["termux-setup-storage"], check=True)


        elif env == "linux":
            print(f"{bold}Installing dependencies for Linux{reset}")
            subprocess.run(["sudo", "apt", "update", "-y"], check=True)
            subprocess.run(["sudo", "apt", "install","aria2", "-y"], check=True)
            subprocess.run(["sudo", "apt", "install", "python3", "ruby-full", "lolcat", "curl", "-y"], check=True)
            subprocess.run(["pip3", "install", "beautifulsoup4", "requests", "lxml"], check=True)

    except:
        pass


def art():
    version = "24.12.20"
    art = r'''
      (\_/)    {0}turboGranny{1} v{2}
     ( •_•)    Downloading dependencies
    / >♥< \    
    '''.format(bold, reset, version)
    subprocess.run(f"echo \"{art}\"", shell=True)
    

if __name__ == "__main__":
    main()