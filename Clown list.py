import requests, os, time

from console.utils import set_title
from datetime import datetime
from pystyle import *
from os import *

clown_banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠋⠁⠀⠉⠻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠁⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠇⠀⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣀⣤⣤⣤⣤⣤⣤⣄⣸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠞⠋⠉⠀⠀⢀⣀⣀⠀⠀⠈⠉⠙⠳⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⡴⢶⣤⣀⣤⣄⠀⠀⠀⠀⠀⠀⣿⣠⡴⠾⠛⠛⠉⠉⠉⠉⠛⠓⠶⣦⣄⣽⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⡏⠀⠀⠈⠉⠀⠙⠛⠛⠳⣆⣠⠾⠋⠁⣀⢤⠀⠀⠀⠀⠀⠀⠀⠀⡤⣀⠉⠛⢶⣄⠀⠀⣼⠛⠻⣶⠞⠛⢶⡄⠀⠀
⠀⣠⣼⣷⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⠁⠀⢠⠞⠁⠘⡇⠀⠀⠀⠀⠀⠀⢸⠁⠈⢳⡀⠀⠙⣷⡶⠟⠀⠀⠈⠀⠀⢠⡟⠀⠀
⣸⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⠁⠀⠀⠘⠂⣄⣚⠁⠀⠀⠀⠀⠀⠀⠈⢓⣤⠔⠛⠀⢰⣏⠀⠀⠀⠀⠀⠀⠀⠙⠛⠻⣦
⠹⣦⣀⠀⠀⠀⠀⠀⠀⠀⣤⣤⠟⠀⠀⠀⣰⣿⣿⠉⣱⡄⠀⠀⠀⠀⢠⢾⣿⡏⠙⣆⠀⠀⢹⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽
⠀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠉⣷⠀⢀⠤⢄⣻⡙⠿⠟⣩⠇⢀⣀⣀⠀⠸⣜⠻⠿⢋⣟⡠⠄⡘⢷⣤⡄⠀⠀⠀⠀⠀⣀⣴⠟
⠀⠹⢦⣴⠀⠀⠀⠀⠀⠠⣶⡟⢰⠁⠀⠀⢹⠉⠓⠛⣡⠞⠛⠉⠉⠛⢷⣌⠙⠚⠉⡏⠀⠀⠈⣿⡁⠀⠀⠀⠀⠀⠀⢻⡅⠀
⠀⠀⠀⢿⡀⠀⠀⠀⠀⠀⣸⠇⠈⠢⣀⣠⠜⠀⠀⣸⠏⠀⠀⠀⠀⠀⠀⢻⡆⠀⠀⠳⡄⠀⠜⠙⢳⡆⠀⠀⣀⣀⣀⣼⠃⠀
⠀⠀⠀⠈⠙⠛⠷⣤⡴⢾⣏⠀⠀⠀⡞⠉⠉⠓⠦⣿⡀⠀⠀⠀⠀⠀⠀⢸⣷⠖⠉⠉⠙⡆⠀⠀⠀⣿⣤⡾⠋⠉⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡀⠀⠀⣇⠀⠰⡀⠀⠈⢷⣄⠀⠀⠀⢀⣠⡟⠁⠀⡰⠃⠀⡎⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⡀⠀⠸⡄⠀⠙⢦⡀⠀⠉⠛⠳⠚⠛⠁⠀⢀⠜⠁⠀⡼⠁⠀⢠⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⣄⠀⠘⢦⡀⠀⠙⠲⢤⣀⣀⣀⣀⡤⠖⠁⠀⣠⠞⠁⠀⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⡀⠙⠲⢄⣀⠀⠀⠀⠀⠀⠀⣀⡤⠚⠁⢀⣤⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠶⣤⣀⣈⠉⠉⠉⠉⠉⠉⣀⣀⣤⠾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
   ___ _                         __ _     _   
  / __\ | _____      ___ __     / /(_)___| |_ 
 / /  | |/ _ \ \ /\ / / '_ \   / / | / __| __|
/ /___| | (_) \ V  V /| | | | / /__| \__ \ |_ 
\____/|_|\___/ \_/\_/ |_| |_| \____/_|___/\__|                    
"""

people_select = """
🤡 Clowns:

[1] Pratik Sen

Select a person from the list with the associated number next to them.
"""

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    os.system('pause >nul')

def main_title():
    set_title("🤡 Clown List | By Bloody | Main")

def print_banner(): 
    print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter(clown_banner)))

def person_select():
    Write.Print(f"{people_select}\n", Colors.purple_to_blue, interval=0.000000001)

def input_number():
    now = datetime.now()
    timenow = now.strftime("%H:%M:%S")
    inp_num = Write.Input(f"[{timenow}] | 🤡 Clown Number: ", Colors.purple_to_blue, interval=0.008)

    if inp_num == "1":
        Write.Print(f"[{timenow}] | 🤡 Chosen Clown: Pratik Sen.", Colors.red_to_blue, interval=0.008)
        time.sleep(2)
        pratik()

def pratik():
    cls()
    print_banner()
    set_title("🤡 Clown List | By Bloody | Clown 1: Pratik")
    Write.Print("🤡 Clown: Pratik Sen\n\nPratik you're literally dog water at Valorant my guy. Bro's a f*cking plastic rank Viper main with only 1 cringe lineup.\nYou're so f*cking dishonest too man.", Colors.red_to_blue, interval=0.0001)
    pause()
    return main()

def main():
    cls()
    main_title()
    print_banner()
    person_select()
    input_number() 
    # And yes everything had to be defined above and used like this here LMAO

# Running main() now
main()