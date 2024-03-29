from colorama import Fore
from itertools import cycle

WS_SERVER_HOST = "127.0.0.1"

LOAD_BALANCER_SERVER_PORT = 5555


SERVER_SIDE_PORT_1 = 7777

SERVER_SIDE_PORT_2 = 8888

SERVER_SIDE_PORT_3 = 9999

SERVER_POOL = [(WS_SERVER_HOST, SERVER_SIDE_PORT_1),
               (WS_SERVER_HOST, SERVER_SIDE_PORT_2),
               (WS_SERVER_HOST, SERVER_SIDE_PORT_3)
              ]

ITERATION = cycle(SERVER_POOL)

sep = "<SEPARATOR>" 

colors = [ Fore.LIGHTCYAN_EX, Fore.WHITE, Fore.CYAN, Fore.GREEN,
           Fore.LIGHTYELLOW_EX, Fore.RED, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX,
           Fore.YELLOW, Fore.BLUE, Fore.LIGHTWHITE_EX,
           Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.MAGENTA
         ]

class Payload:
    message = "Generic message!"
    mode = "group"
    targetId = ""
    request = ""
