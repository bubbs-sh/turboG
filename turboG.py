"""
Author: Prince Addai Desmond @bubbs.sh
Date: 2024-12-31
Description: turboG or turboGranny is a command-line Python utility that scrapes 
             torrent websites,retrieves .torrent files, and automatically launches 
             a torrent client to begin downloading movies. 
             It is designed use on Linux and Termux environments, offering a simple 
             and fast way to download movies directly from the terminal. :)
"""

#! /usr/bin/env python3

from bs4 import BeautifulSoup
import os
import platform
import subprocess
import sys
import time
import requests

tmp_dir = "./.tmp/files"

# Colors variables
bold = "\033[1m"
bold_white = "\033[1;97m"
gray = "\033[1;37m"
red = "\033[1;91m"
blue = "\033[1;94m"
yellow = "\033[1;93m"
reset = "\033[0m"



def main():
    try:
        art()
        args = sys.argv[1:]
        query = '+'.join(args)

        movie, title = scrape_page(query)
        if movie == "none":
            print("Couldn't load movie's data")
            sys.exit(2)

        name, url = scrape_movie(movie)
        if url == "none":
            print("Couldn't load movie's sources")
            sys.exit(3)
            
        clean(tmp_dir)
        os.makedirs(tmp_dir, exist_ok=True)
        os.chmod(tmp_dir, 0o755)

        try:
            name = name.split("/")
            name = "-".join(name)
        except:
            pass
        filename = f"{name}.torrent"
        path = os.path.join(tmp_dir, filename)

        try:
            subprocess.run(["curl", "-o", path, url])
            time.sleep(1)
            download_path = get_download()
            time.sleep(1)

            try:
                unhide(download_path, title)
                subprocess.run(["aria2c", "-d", download_path, path, "--allow-overwrite=true"], check=True)
                
                hide(download_path, title)
                clean(tmp_dir)
                print("\n\nOpen Downloads folder. Have fun!♥")
                exit()
            except subprocess.CalledProcessError as e:
                clean(tmp_dir)
                hide(download_path, title)
                print(f"An error occurred while downloading with: {e}")
            except FileNotFoundError:
                clean(tmp_dir)
                hide(download_path, title)
                print(f"Error: aria2 is not installed.\n Please run: {bold}python3 setup.py{reset} to install missing dependencies")

        except subprocess.CalledProcessError as e:
            clean(tmp_dir)
            hide(download_path, title)
            exit()
        except Exception as e:
            clean(tmp_dir)
            hide(download_path, title)
            exit()

    except requests.exceptions.ConnectionError:
        clean(tmp_dir)
        hide(download_path, title)
        print(f"{red}Connect to the internet 🥲{red}")
        sys.exit(1)
    except KeyboardInterrupt:
        hide(download_path, title)
        
        clean(tmp_dir)
        print("\nBai Baii ♥")
        sys.exit(0)
    except Exception:
        clean(tmp_dir)
        hide(download_path, title)
        exit(1)


# Deletes donwloaded torrents
def clean(tmp_dir):
    if os.path.exists(tmp_dir):
        files = os.listdir(tmp_dir)
        if files:
            for file in files:
                file_path = os.path.join(tmp_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    pass



# Scrapes the initial page
def scrape_page(query):
    url = f"https://yts.mx/browse-movies/{query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")


    titles = []
    links = []
    # Prints out each movie(title to titles list and link to links list) 
    for movie in soup.find_all('div', class_ = 'browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4') :
        title = movie.find('div', class_ = 'browse-movie-bottom').text.splitlines()
        link = movie.find('a', class_ = 'browse-movie-link') ['href']
        
        titles.append(f"{title[1]} - {title[2]}")
        links.append(link)

    # Prints out each title in titles and link in links
    count = 1
    for title in titles:
        print(f"[{count:02}]  {bold}{title}{reset}")
        print()
        count += 1 
    
    print(f"{red}[{count:02}] Exit{reset}")
    print()
    print()

    while True:
        number = int(input(f"{blue}Select a movie[01 - {count-1:02}]: {reset}"))
        if not(number > count) and (number > 0):
            break 

    if number == count:
        print("\nBai Baii ♥")
        sys.exit(0)

    for i in range(len(links)):
        if number == i+1:
            return links[i], titles[i]
    return "none"



# Scrapes the movie page
def scrape_movie(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find('p', class_ = 'hidden-md hidden-lg')

    titles = []
    torrents = []
    a_tags = data.find_all('a')
    for a in a_tags:
        title = str(a['title'])
        torrent = str(a['href'])

        if not("subtitles" in title.lower() or "subtitles" in torrent.lower()):
            titles.append(title)
            torrents.append(torrent)
        
    if len(titles) == len(torrents):
        count = 1
    else:
        print("Sumn's wrong, fs")
    
    print(f"\n{yellow}Available Sources:{reset}\n")
    for title in titles:
        if "Torrent" in title:
            title = title.replace("Torrent", "")
        print(f"[{count:02}]  {bold}{title}{reset}")
        print()
        count += 1

    print(f"{red}[{count:02}] Go back{reset}")
    print()
    print()
    
    number = input(f"{blue}Select a resolution to download[01 - {count-1:02}]: {reset}")
    while True:
        while not number.isnumeric():
            number = input(f"Select a resolution to download[1 - {count-1}]: ")

        number = int(number)
        if not(number > count) and (number > 0):
            break 

    if number == count:
        print("\n🔙 {}BACK{}\n".format(red,reset))
        main()

    for i in range(len(torrents)):
        if number == i+1:
            return titles[i] ,torrents[i]
    return "none" , "none"



# Gets download path
def get_download():
    linux = os.path.expanduser("~/Downloads")
    termux = os.path.expanduser("~/storage/downloads")

    if os.getenv("TERMUX_VERSION") and os.path.exists(os.path.expanduser("~/storage")):
        return termux
    elif os.path.exists(os.path.expanduser(("~/Downloads"))):
        return linux



# Just read the code. Its really conspicuous
def detect_env():
    if os.path.exists("/data/data/com.termux/files/usr/bin/pkg"):
        return "termux"
    elif platform.system().lower() == "linux":
        return "linux"
    else:
        return "unknown"



# Hides the log files in download path
def hide(path, title):
    title = title.split('-')
    ext = "aria2"
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            if title[0] in file and ext in file and not str(file).startswith('.'):
                file_path = os.path.join(path,file)
                hidden_path = os.path.join(path, f".{file}")
                try:
                    os.rename(file_path, hidden_path)
                except:
                    pass



# Opposite of hide
def unhide(path, title):
    title = title.split('-')
    ext = "aria2"
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            if title[0] in file and ext in file and str(file).startswith('.'):
                hidden_path = os.path.join(path,file)
                file_path = os.path.join(path, file[1:])
                try:
                    os.rename(hidden_path, file_path)
                except:
                    pass          



# Skip :)
def art():
    try:
        desc = "Fast and Simple Movie Downloader"
        version = "25.01.01"
        author = "https://github.com/bubbs-sh/"
        art = r'''
      (\_/)    {3}turboGranny{4} v{0}
     ( •_•)    {1}
    / >♥< \    ~ {2} ~
        '''.format(version, desc, author, bold, reset)
        subprocess.run(f"echo \"{art}\" | lolcat", shell=True)
    except FileNotFoundError:
        print(f"Missing dependencies, please install them.\nExecute: {bold}python3 install.py{reset}")  
    except KeyboardInterrupt:
        pass
    except Exception:
        pass     

if __name__ == "__main__":
    main()