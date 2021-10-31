from colorama import init, Fore, Back, Style
init()

def cout(msg, nl = True):
    if nl:
        print(Fore.GREEN + "[KRONOS] " + Style.RESET_ALL + str(msg))
    else:
        print(Fore.GREEN + "[KRONOS] " + Style.RESET_ALL + str(msg), end='')
        
def cwarn(msg):
    print(Fore.YELLOW + "[KRONOS] " + str(msg))

def cerr(msg):
    print(Fore.RED + "[KRONOS] " + str(msg))

def yes_or_no(question):
    cout(question, False)
    reply = str(input(' (y/N): ')).lower().strip()
    if len(reply) > 0 and reply[0] == 'y':
        return True
    else:
        return False