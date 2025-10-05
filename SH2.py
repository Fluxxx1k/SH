# logging ТГ
import time as t
import os
import sys
import random as rnd
import platform
from atexit import register as atexit
release = platform.release()

ff = __file__
print(ff)
LIGHT_BLUE = pres = '\033[36m'  # WHITE_BLUE
YELLOW = chanc_color = '\033[33m'  # YELLOW
BLUE = BASE = '\033[34m'  # BLUE
PURPLE = DEBUG = '\033[35m'  # PURPLE
RED = '\033[31m'
BLACK = '\033[32m'  # GREEN
END = '\033[0m'
DBG_B = '\033[1m' + DEBUG
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
GREY = '\033[37m'
saved = []
DEAD = '\033[41m'  # RED_FONT
GULAG = '\033[43m'  # YELLOW_FONT
BLACK_FONT = '\033[40m'
BLUE_FONT = BASE_FONT = '\033[34m'
NAME_FOR_LOGS = "SH LOG_TEST "  # You can change it
tp = '.html'  # расширение
path = os.path.dirname(ff) + '/'
date = t.strftime("%d.%m.%y ")
MAX_NAME_LEN = 15  # You can change it from 10 to infinity
#if 'android' in release.lower() or 'lineageos' in release.lower():
#    WHITE = '\033[37m'
#    print(f"{YELLOW}Launched on Android{END}")
#else:
#    WHITE = '\033[38m'
WHITE = '\033[97m'
LEN_FOR_TABLET = MAX_NAME_LEN + len(pres + WHITE)
pr_c = 'cyan'
ch_c = 'yellow'
red_c = 'red'
black_c = 'lime'
nrh_c = 'DeepSkyBlue'
purple_c = 'DarkViolet'
num_c = "orange"
norm_c_cut = 'white'
font_c_cut = 'black'
norm_c = '"' + norm_c_cut + '"'
font_c = '"' + font_c_cut + '"'
vnf = False
skips = 0
logs: list[tuple[tuple[str, str], tuple[str, str, str, str]]] = []
Git_not = set()
g = []  # GAYmers

print(f"If 1 of this colors is blue say it to coder (DS: {PURPLE}@fluxxx1k{END}): {BLUE}{WHITE}ABC{BLUE}{GREY}ABC{END}")

# Number of players and their names
while True:
    try:
        c = int(input(f"Input number of players: {DBG_B}"))
        print(END, end='')
        if c < 4 or c > 10:
            raise Exception("Wrong size!")
    except BaseException as err:
        print(f"{RED}Try again, wrong input: {err}{WHITE}")
    else:
        if not input(f"If you are sure that here will be {c} gamers press ENTER else write anything: "):
            break
if c == 6:
    print(f"{DBG_B}5 {RED}RED{DEBUG} cards, 11 {BLACK}BLACK{DEBUG} cards{END}")
    red_start = 5
    black_start = 11
else:
    print(f"{DBG_B}6 {RED}RED{DEBUG} cards, 11 {BLACK}BLACK{DEBUG} cards{END}")
    red_start = 6
    black_start = 11
deck = ['R'] * red_start + ['B'] * black_start
check_logs = os.listdir(path)
logs_nums = []
gulag = c
killed = c
roles = [f"{BLACK}HITLER{END}"] + [f"{BLACK}BLACK{END}" * (1 if c < 7 else 2)]
roles.extend([f"{RED}RED{END}"] * (c - len(roles)))
rnd.shuffle(roles)
hitler = roles.index(f"{BLACK}HITLER{END}")
stalin = c
try:
    stalin = roles.index(f"{RED}STALIN{END}")
except:
    print("No Sosalin :_((")


for i in check_logs:
    if i[:len(NAME_FOR_LOGS) + len(date)] == NAME_FOR_LOGS + date:
        logs_nums.append(i)
max_log_num = len(logs_nums) + 1
full_path = path + NAME_FOR_LOGS + date + str(max_log_num) + tp
while os.path.exists(full_path):
    max_log_num += 1
    print(RED + BOLD + UNDERLINE + path + NAME_FOR_LOGS + date + str(max_log_num) + tp +
          "    is already exists, trying {pres}{max_log_num}{END}")
    full_path = path + NAME_FOR_LOGS + date + str(max_log_num) + tp
print("Logs in:", full_path)
start_time = t.strftime("Game start time:   %d.%m.%y %H:%M:%S")
print(start_time)
logged = 0
red = black = 0
checks = 1
Git_caput = False
Git_cn = False
f_l = {"OUT", "DEBUG_MODE", "EXIT"}
molotov_ribbentrop = True


def out(file=sys.stdout):
    for i in range(c):
        print(f"№{i + 1}) {g[i].out()}", file=file)


def coloring(s, sort=True):
    if sort:
        s = sorted(s)
    s1 = ''
    for i in s:
        if i in {"B", "H"}:
            s1 += BLACK + i + WHITE
        elif i in {'R', 'S'}:
            s1 += RED + i + WHITE
        elif i == 'X':
            s1 += i
        else:
            print(f"{i} should be 'X' or 'R' or 'B'")
    return s1


# def add_2_logs(x, y, a, b, c):
#    logs.append(((x,y)()))


def dbg(s):
    s = s.split()
    if s[0] == 'ccp':
        global ccp
        ccp = coloring(s[1])
    elif s[0] == 'ccs':
        global ccs
        ccs = coloring(s[1])
    elif s[0] == 'cps':
        global cps
        cps = coloring(s[1])
    else:
        print("{RED}Wrong parameters{WHITE}")

@atexit
def logs_out():
    create_HTML_logs()
    return
    with open(full_path, 'r', encoding='UTF-8') as f:
        r = f.read()
    r = r[:r.find('-' * 20)] + '\n'
    log = 1
    try:
        f = open(full_path, "w+", encoding="UTF-8")
        print(r, file=f)
        print('-' * 20, file=f)
        print(
            f"{END}{UNDERLINE}{BOLD}| {pres + 'President' + WHITE: <{LEN_FOR_TABLET}} | {chanc_color + 'Chancellor' + WHITE: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}",
            file=f)
        print(
            f"{END}{UNDERLINE}{BOLD}| {pres + 'President' + WHITE: <{LEN_FOR_TABLET}} | {chanc_color + 'Chancellor' + WHITE: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}")
        for i in logs:
            log += 1
            print(
                f"{END}{UNDERLINE}{BOLD}| {pres + i[0][0] + WHITE: <{LEN_FOR_TABLET}} | {chanc_color + i[0][1] + WHITE: <{LEN_FOR_TABLET}} | {i[1][0] + WHITE: <8} | {i[1][1] + WHITE: <7}  | {i[1][2] + WHITE: <6}   | {(i[1][3] if len(i[1]) >= 4 else 'XXX') + WHITE: <8}  |{END}",
                file=f)
            print(
                f"{END}{UNDERLINE}{BOLD}| {pres + i[0][0] + WHITE: <{LEN_FOR_TABLET}} | {chanc_color + i[0][1] + WHITE: <{LEN_FOR_TABLET}} | {i[1][0] + WHITE: <8} | {i[1][1] + WHITE: <7}  | {i[1][2] + WHITE: <6}   | {(i[1][3] if len(i[1]) >= 4 else 'XXX') + WHITE: <8}  |{END}")
    except BaseException as err:
        f = open(full_path, "w+", encoding="UTF-8")
        print(r, file=f)
        print(err, file=f)
        print(err)
        print('-' * 20, file=f)
        log -= 1
        print(
            f"{END}{UNDERLINE}{BOLD}| {pres + 'President' + WHITE: <{LEN_FOR_TABLET}} | {chanc_color + 'Chancellor' + WHITE: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}",
            file=f)
        print(
            f"{END}{UNDERLINE}{BOLD}| {pres + 'President' + WHITE: <{LEN_FOR_TABLET}} | {chanc_color + 'Chancellor' + WHITE: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}")
        for i in logs:
            log -= 1
            if log:
                print(
                    f"{END}{UNDERLINE}{BOLD}| {pres + i[0][0] + WHITE: <{LEN_FOR_TABLET}} | {chanc_color + i[0][1] + WHITE: <{LEN_FOR_TABLET}} | {i[1][0] + WHITE: <8} | {i[1][1] + WHITE: <7}  | {i[1][2] + WHITE: <6}   | {(i[1][3] if len(i[1]) >= 4 else 'XXX') + WHITE: <8}  |{END}",
                    file=f)
                print(
                    f"{END}{UNDERLINE}{BOLD}| {pres + i[0][0] + WHITE: <{LEN_FOR_TABLET}} | {chanc_color + i[0][1] + WHITE: <{LEN_FOR_TABLET}} | {i[1][0] + WHITE: <8} | {i[1][1] + WHITE: <7}  | {i[1][2] + WHITE: <6}   | {(i[1][3] if len(i[1]) >= 4 else 'XXX') + WHITE: <8}  |{END}")
            else:
                print(*i, sep=f'{END} | ', file=f)
                print(*i, sep=f'{END} | ')
    finally:
        f.close()


def input_cards(text="{RED}Some input: {WHITE}", q: int | set[int] = 0, c_p=False, veto=(black >= 5)) -> str:
    """
    c_p - chancellor placing, don't laugh
    """
    if not isinstance(veto, bool):
        print(f"{RED}{BOLD}{UNDERLINE}{veto = } | it's not good!{END}")
        veto = black >= 5
    letters = {'X', 'R', 'B'}
    if q == 0:  # quality didn't change
        print("{RED}{BOLD}{UNDERLINE}Input length is {q = }, it will be 1-3 now")
        q = {1, 2, 3}
    elif not isinstance(q, set):
        q = {q}
    if c_p and not veto:  # chancellor should place card if it wasn't veto
        letters -= {'X'}
    if c_p:  # if president was skipped in game, but not in code 
        letters.add("SKIP")
    inp = input(text + END + DBG_B).strip().upper()
    print(END, end='')
    while len(inp) not in q or (len(letters | set(inp)) > 3 and inp not in letters):
        print(f"{RED}WRONG    INPUT{END}")
        inp = input(DEBUG + "New try: " + WHITE + text + END + DBG_B).strip().upper()
        print(END, end='')
    return inp


def new_gov(gov_type=f"GOVERNMENT", color=BASE):
    while True:
        try:
            gov = int(input(f"{color}{gov_type}{WHITE}'s number (not index): {DBG_B}")) - 1
            print(END, end='')
            if gov >= c or gov < 0 or gov == pn or gov == gulag or gov == killed:
                raise Exception("Wrong number")
        except BaseException as err:
            print(f"{RED}{err}{END}")
        else:
            if not input("ENTER if number is right, else write something: "):
                break
    out()
    return gov


def degov():
    for i in range(c):
        g[i].degov()

    print(f"{DEBUG}  # GOVERNMENT RESETED (dbg){END}")
    # out()


def comm(cmd):
    if cmd.upper() in {"H", "HELP"}:
        print(*sorted(f_l), sep=', ')
        print(f"{RED}May be mistakes{END}")
    if cmd.upper() in {'LOG', 'LOGS'}:
        logs_out()
    elif cmd == "DEBUG_MODE" or cmd == "DBG":
        print(
            f"{END}{DBG_B}To exit from debug mode write \"exit\"\n{END}{RED}{BOLD}DO    NOT    USE{END}{RED}    \"exit()\"    OR    \"Ctrl + D\"{END}")
        try:
            breakpoint()
        except BaseException as err:
            print(err)
        print(END, end='')
    elif cmd == "OUT":
        out()
    elif cmd == '' or name == 'EXIT':
        return True


def show_only_to_one(text, hide_len=0):
    if not hide_len:
        x = False
        for i in text:
            if i != '\033':
                if not x:
                    hide_len += 1
                elif i == 'm':
                    x = False
            else:
                x = True
    print("Are you ready to see info?")
    print("(Remember it. Don't show it to anybody)")
    print("Say \"y\" only if YOU should see them: ")
    if yes_or_no("Show?", no=set()):
        print(text)
    if yes_or_no("Hide? ", no=set()):
        print(f"{END}\x1b[A\x1b[A" + "⣿" * hide_len)
        print()


def take_random(count):
    global saved
    if saved:
        x = saved.copy()
        saved = []
        return x
    global deck
    try:
        chosen = rnd.sample(deck, k=count)
    except ValueError:
        print("DECK RESET")
        logs.append(((DEBUG + f'{"DECK":<{MAX_NAME_LEN}}' + WHITE, DEBUG + f'{"RESET":<{MAX_NAME_LEN}}' + WHITE),
                     ('   ', '  ', ' ', '   ')))
        deck = ["R"] * (red_start - red) + ["B"] * (black_start - black)
        chosen = rnd.sample(deck, k=count)
    for i in chosen:
        deck.remove(i)
    rnd.shuffle(chosen)
    return chosen


def yes_or_no(text='Input for something (If you see it, you should understand what should be asked): ',
              yes: set | frozenset = frozenset({'y', 'Y', 'Y|y', 'yes', 'Yes', 'YES'}),
              no: set | frozenset = frozenset({'N', 'n', 'N|n', 'no', "No", "NO"})):
    inp = input(text + ' ').strip()
    while inp not in yes and inp not in no:
        inp = input('\x1b[A' + f"{DEBUG}{text} New try: {END}").strip()
    if inp in yes:
        return True
    if inp in no:
        return False
    print(f"WTF: {inp}")
    return False


def full_clear(s):
    if isinstance(s, Player):
        return str(s)
    s1 = ''
    x = False
    for i in s:
        if i == '\033':
            x = True
        elif i == 'm':
            x = False
        elif not x:
            s1 += i
    return s1
    
def coloring_HTML_cards(s2):
    s = sorted(full_clear(s2))
    errs = 0
    s1 = ''
    for i in s:
        if i == "B":
            s1 += f"<font color='{black_c}'>" + i + "</font>"
        elif i == 'R':
            s1 += f"<font color='{red_c}'>" + i + "</font>"
        elif i == 'X':
            s1 += f"<font color='{norm_c_cut}'>" + i + "</font>"
        elif i == 'P':
            s1 += f"<font color='{nrh_c}'>" + i + "</font>"
        else:
            print(f"{i} should be 'X' or 'R' or 'B' or 'P'")
            errs += 1
            s1 += f"<font color='{norm_c_cut}'>" + i + "</font>"
    return full_clear(s2) if errs > 0 else s1
    
def get_color(x, out_type=''):
    x = full_clear(x)
    for i in ["BLACK", "HITLER", "RIBBENTROP"]:
        if i in x:
            if out_type == "Bot":
                if i == "HITLER":
                    return "HTLR"
                return "BLK"
            if out_type == "HTML":
                return black_c
            return BLACK+BOLD+"BLACK"+END
    for i in ["RED", "MOLOTOV", "STALIN"]:
        if i in x:
            if out_type == "Bot" :
                return "RED"
            if out_type == "HTML":
                return red_c
            return RED+BOLD+"RED"+END
    if "ANARCHIST" in x:
        if out_type == "Bot" :
                return "NRH"
        if out_type == "HTML":
                return nrh_c
        return BOLD+"ANARCHIST"+END
    else:
        if out_type == "Bot" :
                print(f"{RED}{BOLD}{UNDERLINE}Bot ERR, unknown role... Using {BOLD}ANARHY{RED} type...{END}")
                return "NRH"
        if out_type == "HTML":
                return norm_c
        return BOLD+"ERROR, please, show it in IRL" + END



def coloring_HTML_roles(s):
    s = full_clear(s)
    if s in {"R", "RED"}:
        return f"<font color='{red_c}'>" + "RED" + "</font>"
    if s in {"H", "HITLER"}:
        return f"<font color='{black_c}'>" + "HITLER" + "</font>"
    if s in {"B", "BLACK"}:
        return f"<font color='{black_c}'>" + "BLACK" + "</font>"
    if s in {"S", "STALIN"}:
        return f"<font color='{red_c}'>" + "STALIN" + "</font>"
    if s in {"M", "MOLOTOV"}:
        return f"<font color='{red_c}'>" + "MOLOTOV" + "</font>"
    if s in {"RIB", "RIBBENTROP"}:
        return f"<font color='{black_c}'>" + "RIBBENTROP" + "</font>"
    if s in {"A", "ANARHY", "ANARCHIST"}:
        return f"<font color='{nrh_c}'>" + "ANARCHIST" + "</font>"
    if s in {"X", "UNKNOWN", "IDK"}:
        return f"<font color='{norm_c}'>" + "UNKNOWN" + "</font>"
    print("UNKNOWN    ROLE")
    return "???"



def create_HTML_roles():
    s = '<table>\n<caption><h1><b>Таблица ролей<br>Table of roles<b></h1></caption>'
    table_header = f"<tr><th>Number</th><th>Player</th><th>Role</th></tr>\n"
    s += table_header
    rows = []
    try:
        roles
    except NameError:
        print("Old version")
        try: 
            roles = colors
        except BaseException as err:
            print(f"Too old version or smth else: {err}")
    except BaseException as err:
        print(f"Too old version or smth else: {err}")
    try:
        for i in range(c):
            number = f"<td style=\"color: {num_c}\"><b>{i+1}</b></td>"
            player = f'<td style="color: {get_color(full_clear(roles[i]), out_type="HTML")}"><b>{g[i]}</b></font></td>'
            role = f'<td><b>{coloring_HTML_roles(full_clear(roles[i]))}</b></td>'
            row = "<tr>" + number + player + role + "</tr>"
            rows.append(row)
        s += '\n'.join(rows)
    except BaseException as r:
        print(f"No roles, old version or using cards: {r}")
        return ''
    s += '\n</table>'
    return s

def create_HTML_logs():
     s = ''
     head = """
     <head>
         <meta charset='UTF-8'>
         <title>Secret Hitler logs</title>
         <style>
         body {
         color:""" + norm_c_cut + """;
         background-color: """ + font_c_cut + """;
         }
         table {
         border:5px solid """ + norm_c_cut + """;
         <!-- bgcolor: black; -->
         padding: 10px;
         cellpadding: 10px;
         cellspacing: 2px;
         border-collapse: collapse;
         width: 100%;
         margin-bottom: 20px;
         }
         th {border: 3px """ + norm_c_cut + """ solid;}
         td {border: 2px """ + norm_c_cut + """ solid;}
         </style>
     </head>
     """
     body = """
     <body>"""
     table_roles = create_HTML_roles()
     table ="""    <table>\n<caption><h1><strong>Таблица событий игры<br>Logs of the game </strong></h1></caption>
             """
     table_header = f"<tr><th>N</th><th color={pr_c}>President</th><th color={ch_c}>Cancler</th><th>CPS</th><th>CCS</th><th>CCP</th><th>CPSA</th></tr>"
     table += table_header
     rows = []
     for i in range(len(logs)):
         log=logs[i]
         try:
             cpsa = log[1][3]
         except:
             cpsa = ""
         number = f'<td style="color: {num_c}">{i+1}</td>'
         president = f'<td style="color: {pr_c if full_clear(log[0][0]) in map(full_clear, g) else purple_c}"><b>{full_clear(log[0][0])}</b></td>'
         chancellor = f'<td style="color: {ch_c if full_clear(log[0][1]) in map(full_clear, g) else purple_c}"><b>{full_clear(log[0][1])}</b></td>'
         cps = f"<td><b>{coloring_HTML_cards(log[1][0])}</b></td>"
         ccs = f"<td><b>{coloring_HTML_cards(log[1][1])}</b></td>"
         ccp = f"<td><b>{coloring_HTML_cards(log[1][2])}</b></td>"
         cpsa = f"<td><b>{coloring_HTML_cards(cpsa)}</b></td>"
         row = "<tr>" + number +  president + chancellor + cps + ccs + ccp + cpsa + '</tr>'
         rows.append(row)
     table += '\n'.join(rows)
     table += "\n</table>"
     body += table_roles + '\n' + table
     body+="""
     </body>
     """
     s = """
    <!DOCTYPE html>
    <html>""" 
    
     s += head+body
     s += "</html>"
     with open(full_path, 'w+', encoding = "UTF-8") as f:
         print(s, file=f)
         print(s)


def weighted_random(a, weights):
    return rnd.choices(a, weights, k=1)[0]



class Player:
    base_name = "Player"

    def __init__(self, num, name="RANDOM", role=f"{DEBUG}ANARCHIST{END}"):
        self.gov_pref = ''
        self.gov_suff = ''
        self.purge_pref = ''
        self.purge_suff = ''
        self.num = num
        self.role = role
        self.color = get_color(self.role)
        self.prefix = ''
        self.suffix = ''
        if name != "RANDOM":
            self.name = ' '.join(name.split())
        else:
            self.name = Player.base_name + str(num)
        self.tablet_name = f"{self.name: <{MAX_NAME_LEN}}"
        self.dark = 0

    def __repr__(self):
        s = f"{self.name= } ({self.tablet_name= }): {self.role= } (mind_type: {self.color= }), {self.dark= }"
        # {len(self.name) == MAX_NAME_LEN = }
        return s

    def __add__(self, s):
        self.suffix += s
        return self

    def __radd__(self, s):
        self.prefix += s
        return self

    def __str__(self):
        return self.prefix + self.name + self.suffix

    def __eq__(self, other):
        if type(other) == str:
            if self.name == other:
                return True
            return False
        if self.name == other.name:
            return True
        return False

    def __lt__(self, other):
        if self.dark < other.dark:
            return True
        return False

    def __le__(self, other):
        if self.dark <= other.dark:
            return True
        return False

    def __gt__(self, other):
        if self.dark > other.dark:
            return True
        return False

    def __ge__(self, other):
        if self.dark >= other.dark:
            return True
        return False

    def __format__(self, args):
        return str(self).format(*args)

    def degov(self):
        self.gov_suff = ''
        self.gov_pref = ''
    #def president(self, card, cnc):
    def get_color(self):
        return self.color
    def free(self, ask=True):
        x = (self.num == gulag) + (self.purge_pref == GULAG)
        if x == 2:
            print(f"{self.name} freed")
            gulag = c
            self.purge_pref = self.purge_suff = ''
        elif x == 1:
            print(f"Err: {self.purge_pref= }, {(self.purge_suff==GULAG) = }, but {(gulag == self.num) = }")
            if yes_or_no("Free him?"):
                gulag = c
                self.purge_pref = self.purge_suff = ''
        elif ask:
            print(f"Err: {self.purge_pref= }, {(self.purge_suff==GULAG) = }, but {(gulag == self.num) = }")
            print("And you tried to free him.")
            if yes_or_no("Try to free all another?"):
                for player in g:
                    player.free(ask=False)
    def chosen_gov(self, gov_type:'president' or 'chancellor'):
        if gov_type == 'president':
            self.gov_pref = pres  
        elif gov_type == 'chancellor':
            self.gov_pref = chanc_color
        else:
            self.gov_pref = BASE
            print(f"Uncknown government type: {gov_type}")
        self.gov_suff = WHITE
    def purge(self, purge_type:'gulag' or 'killed'):
        if purge_type == 'gulag':
            self.purge_pref = GULAG
            global gulag
            gulag = self.num
        elif purge_type == 'killed':
            global killed
            killed = self.num
            self.purge_pref = DEAD
        
        self.purge_suff = BLACK_FONT
    def president(self, card, cnc):
        show_only_to_one(f"Remember, your role is {self.role}, color is {self.color}.")
        card1 = coloring(card)
        print(card1)
        phrase = f"You will say that here: "
        words = input(phrase).strip().upper()
        while len(words) != 3 or not set(words).issubset({'X', "B", "R"}):
            words = input('\x1b[A' + phrase).strip().upper()
        print(f'\x1b[A{phrase}{coloring(words)}')
        phrase1 = f"You will give to chancellor ({g[cnc]}): "
        to_cnc = input(phrase1).strip().upper()
        while len(to_cnc) != 2 or not set(to_cnc).issubset(set(card)):
            to_cnc = input('\x1b[A' + phrase1).strip().upper()
        print('\x1b[A\x1b[A\x1b[A' + "⣿"*len(card))
        print()
        print(phrase1 + '⣿' * len(to_cnc))
        return words, to_cnc, yes_or_no("Veto? ") if black == 5 else False
        
    def chancellor(self, card, prs, words, veto):
        show_only_to_one(f"Remember, your role is {self.role}, color is {self.color}.")
        card1 = coloring(card)
        print(card1)
        phrase = f"You will say that here: "
        words = input(phrase).strip().upper()
        while len(words) != 2 or not set(words).issubset({'X', "B", "R"}):
            words = input('\x1b[A' + phrase).strip().upper()
        print(f'\x1b[A{phrase}{coloring(words)}')
        phrase1 = f"You will place: "
        placed = input(phrase1).strip().upper()
        while len(placed) != 1 or placed not in cards or (placed != "VETO" and veto):
            placed = input('\x1b[A' + phrase1).strip().upper()
        
        print('\x1b[A\x1b[A\x1b[A' + "⣿"*len(card))
        print()
        if placed == "VETO":
            return words, "X"
        print(phrase + coloring(placed))
        return words, placed
        
    def table(self):
        return self.gov_pref + self.purge_pref + self.prefix + self.tablet_name + self.gov_suff + self.purge_suff + self.suffix 
    def out(self):
        return self.gov_pref + self.purge_pref + self.prefix + self.name + self.gov_suff + self.purge_suff + self.suffix 
    
class Bot(Player):
    base_name = "Bot"

    def __init__(self, num="ERR", role=f"{DEBUG}ANARCHIST{END}",
                 name="RANDOM",
                 ):
        super().__init__(num, role, name)
        self.bot_mind = get_color(self.role, out_type='Bot')
        self.risk = rnd.random()
        self.black = []
        if self.color == 'BLK':
            for i in range(c):
                if g[i].color == 'BLK':
                    self.black.append(i)
            

    def __repr__(self):
        s = super().__repr__()
        s += " "
        s += f"[BOT INFO: {self.bot_mind= }, {self.dark= }, {self.risk= }]"
        return s

    def president(self, card, cnc) -> tuple[str, list[str], bool]:
        card = sorted(card)
        if self.bot_mind == 'HTLR':
            if card == ["R", "R", "R"]:
                return "XXX", ["R", "R"], black == 5
            if card == ["B", "R", "R"]:
                return "XXX", ["B", "R"], False
            if card == ["B", "B", "R"]:
                if rnd.random() < 0.9 or red == 4 or black == 5:
                    return "XXX", ["B", "B"], False
                else:
                    return "XXX", ["B", "R"], False
            if card == ["B", "B", "B"]:
                return "XXX", ["B", "B"], False
        if self.bot_mind == "BLK":
            if card == ["B", "R", "R"]:
                return "XXX", ["B", "R"], False
            if card == ["B", "B", "R"]:
                if rnd.random() < 0.96 or red == 4 or black == 5:
                    return "XXX", ["B", "B"], False
                else:
                    return "XXX", ["B", "R"], False
            if card == ["B", "B", "B"]:
                return "XXX", ["B", "B"], False
            if card == ["R", "R", "R"]:
                return "XXX", ["R", "R"], black == 5
            print("Unknown situation {card= }")
            return "XXX", card[:2], black == 5
        if self.bot_mind == "RED":
            if card == ["B", "R", "R"]:
                if red == 4 or black == 5:
                    return "XXX", ["R", "R"], False
                else:
                    if cnc in self.black:
                        return "XXX", ["R", "R"], False
                    return "XXX", ["B", "R"], False
            if card == ["B", "B", "R"]:
                return "XXX", ["B", "R"], False
            if card == ["R"] * 3:
                return "XXX", ["R"] * 2, False
            if card == ["B"] * 3:
                return "XXX", ["B"] * 2, black == 5
            print("Unknown situation {card= }")
            return "XXX", card[1:], black == 5
        if self.bot_mind == "NRH":
            if "B" in card and "R" in card:
                return "XXX", ["B", "R"], black == 5
            else:
                return "XXX", card[1:], black == 5
        else:
            print(f"Unknown {self.bot_mind= }")
            if "B" in card and "R" in card:
                return "XXX", ["B", "R"], black == 5
            else:
                return "XXX", card[1:], black == 5

    def chancellor(self, card, prs, words, veto) -> tuple[str, str]:
        card = sorted(card)
        if self.bot_mind == "RED":
            if "R" in card:
                return "XX", "R"
            elif veto:
                return "XX", "X"
            else:
                return "XX", 'B'
        if self.bot_mind == "HTLR":
            if red == 4 or black == 5:
                if "B" in card:
                    return "XX", "B"
                if veto:
                    return "XX", 'X'
                return "XX", "R"
            if "B" in card and prs in self.black and (words == "BBB" or words == "XXX"):
                return "XX", "B"
            else:
                return "XX", "R"
        if self.bot_mind == "BLK":
            if card == ["B"] * 2:
                return "XX", "B"
            if card == ["R"]:
                if veto:
                    return "XX", 'X'
                return "XX", "R"
            if red == 4 or black == 5:
                return "XX", "B"
            if prs in self.black and (words == "BBB" or words == "XXX"):
                return "XX", "B"
            if red == 3:
                if rnd.random() < 0.69:
                    return "XX", "R"
                return "XX", "B"
            if rnd.random() < 0.96:
                return "XX", "R"
            return "XX", "B"
        else:
            if self.bot_mind != "NRH":
                print("Unknown role {self.bot_mind= }")
            if red <= black:
                if "R" in card:
                    return "XX", "R"
                return "XX", "B"
            else:
                if "B" in card:
                    return "XX", "B"
                return "XX", "R"


#    def check_color(self):
#        x = weighted_random(g, list(map(Player.dark, g)))
#        if self.bot_mind == "RED":
#            return x.name, x.color
#        if self.bot_mind = "BLK":
#        
#    def check_cards(self,  card):
#        print(coloring("BBB"))


for i in range(c):
    name = input(f"GAYmer №{i + 1}) {DBG_B}")
    print(END, end='')
    while len(name) > MAX_NAME_LEN or name == '' or name in g:
        print(f"{RED}Length of name should be 1-{MAX_NAME_LEN} symbols!{END}")
        name = input(f"{RED}New attempt:{END} GAYmer №{i + 1}) {DBG_B}")
        print(END, end='')

    g.append(Player(num=i, name=name, role=roles[i]))
err = []
while True:
    try:
        err = list(map(int, input(f"Print numbers of mistakes: {DBG_B}").split()))
        print(END, end='')
        for i in err:
            if i > c or i < 1:
                raise Exception
    except:
        print(f"{RED}Wrong syntax or too big nums{END}")
    else:
        break
for i in err:
    name = input(f"{DEBUG}Fixing names:{END} GAYmer №{i}) {DBG_B}").strip()
    print(END, end='')
    while len(name) > MAX_NAME_LEN or name == '' or name in g:
        print(f"{RED}Length of name should be 1-{MAX_NAME_LEN} symbols!{END}")
        name = input(f"{RED}New try:{END} GAYmer №{i}) {DBG_B}").strip()
        print(END, end='')
    g[i - 1].name = name
print(*list(map(repr, g)), sep='\n')

with open(full_path, 'a+', encoding='UTF-8') as f:
    print(start_time, file=f)

with open(full_path, 'a+', encoding="UTF-8") as f:
    for i in range(c):
        print(f"{PURPLE}{DBG_B}[{g[i]}]{END}, come here to get your role!")
        show_only_to_one(f"Your role is: {DBG_B}{roles[i]}{END}", 25)
        print(f"№{i + 1} ({g[i]}) was {roles[i]}", file=f)

while True:
    try:
        pn = int(input(f"{pres}President{END}'s number (not index): {DBG_B}")) - 1
        print(END, end='')
        if pn >= c or pn < 0:
            raise Exception
    except BaseException as err:
        # print(err)
        print(f"{RED}Wrong syntaxis or too big/small nums{END}")
    else:
        if not input("ENTER if number is right, else write something: "):
            break
pn -= 1
pnc = pn
while red < 5 and black < 6 and not Git_caput and not Git_cn:
    if pnc != pn:
        if vnf:
            print(f"{DEBUG}{pnc = } != {pn = } => Внеоф{WHITE}")
        else:
            # print(f"{DEBUG}WTF?!! (Line 160)")
            print(f"{DEBUG}{pnc = } != {pn = } but {vnf = }{WHITE}")
            pn = pnc
    if skips > 2:
        if yes_or_no(f"Anarchy? (Skips: {skips}): "):
            ccp = take_random(1)[0]
            logs.append(((f"{DEBUG + 'SHUFFLED' + WHITE: <{LEN_FOR_TABLET}}",
                          f"{DEBUG + 'CARDS' + WHITE: <{LEN_FOR_TABLET}}"), ('   ', '  ', ' ', '   ')))
            logs.append(((f"{DEBUG + 'ANARCHY' + WHITE: <{LEN_FOR_TABLET}}",
                          f"{DEBUG + 'ANARCHY' + WHITE: <{LEN_FOR_TABLET}}"), ('   ', '  ', coloring(ccp), '   ')))
            if ccp == 'B':
                black += 1
                checks += 1
                if black == 6:
                    degov()
                    break
            elif ccp == 'R':
                red += 1
                if red == 5:
                    degov()
                    break
            else:
                print(f"WTH?!!!! {ccp} isn't 'B' or 'R'")
            saved = 0
            if gulag < c:
                logs.append(((f"{DEBUG + 'ANARCHY' + WHITE: <{LEN_FOR_TABLET}}", g[gulag].tablet()),
                             (f'{DEBUG}FRE{WHITE}', f'{DEBUG}E!{WHITE}', f'{DEBUG}!{WHITE}', '   ')))
                print(f"{DEBUG}{g[gulag]} was de-Gulag-ed{WHITE}")
                g[gulag] = g[gulag][10:-10]
                gulag = c
            logs_out()
    pn = (pn + 1) % c
    if pn == gulag:
        print(f"{DEBUG}President can't be in gulag, next{WHITE}")
        pn = (pn + 1) % c
    if pn == killed:
        print(f"{DEBUG}President can't be dead, next{WHITE}")
        pn = (pn + 1) % c
    if pn == gulag:
        print(f"{DEBUG}President can't be in gulag, next{WHITE}")
        pn = (pn + 1) % c
    g[pn].chosen_gov('president')
    out()
    if not vnf:
        pnc = pn
    else:
        vnf = False
    if yes_or_no(f"Skip? (Skips: {skips}): "):
        skips += 1
        degov()
        print("\n\n\n")
        continue
    else:
        skips = 0

    cn = new_gov("Chancellor", chanc_color)
    if black >= 3 and cn not in Git_not: 
        if c == stalin:
            if cn == hitler:
                degov()
                logs.append(((g[pn].table(), g[cn].table()), (f'{BLACK}HIT{WHITE}', f'{BLACK}LE{WHITE}', f'{BLACK}R{WHITE}', '   ')))
                Git_cn = True
                break
            else:
                Git_not.add(cn)
        else:
            if hitler == cn:
                if yes_or_no("Is {g[cn].name} hitler "):
                    degov()
                    logs.append(((g[pn].table(), g[cn].table()), (f'{BLACK}HIT{WHITE}', f'{BLACK}vs{WHITE}', f'{BLACK}S{WHITE}', 'TAL')))
                    Git_caput = True
                    break
            else:
                yes_or_no("Is {g[cn].name} hitler? ", yes=set())
    g[cn].chosen_gov('chancellor')
    cards = take_random(3)
    cps, cards, veto = g[pn].president(cards, cn)
    ccs, ccp = g[cn].chancellor(cards, pn, cps, veto)
    cpsa = input_cards(f"Cards {pres}president{WHITE} ({g[pn]}) said after chancellor: ", q={3, 0})
    temp = input(f'Command: {DBG_B}').upper()
    print(END, end='')
    while not comm(temp):
        # print(f"{RED}Wrong syntaxis{END}")
        temp = input(f'Command (new try): {DBG_B}').upper()
        print(END, end='')
    if ccp == 'B' or ccp == BLACK + "B" + WHITE:
        black += 1
    elif ccp == 'R' or ccp == RED + "R" + WHITE:
        red += 1
    elif ccp == 'P':
        red += 1
        black += 1
    elif (ccp == 'VETO'  or ccp == "X") and black >= 5:
        print(f"{DEBUG}Passing cuz VETO{WHITE}")
        degov()
        continue
    else:
        print(f"WTH?!!!! {ccp} isn't 'B' or 'R'")
        ccp = 'X'
    cps = coloring(cps)
    ccs = coloring(ccs)
    ccp = coloring(ccp)
    if cpsa:
        cpsa = coloring(cpsa)
    else:
        cpsa = cps

    degov()
    print("\n\n\n")

    logs.append(((g[pn].table(), g[cn].table()), (cps, ccs, ccp, cpsa)))
    if black == 1 == checks:
        saved = take_random(3)
        show_only_to_one(coloring(saved))
        cpsc = input_cards(f"Cards {pres}president{END} said after checking: ", q=3)
        cpsc = coloring(cpsc)
        logs.append(((g[pn].table(), f"{DEBUG + 'CARD CHECK' + WHITE: <{LEN_FOR_TABLET}}"),
                     (cpsc, DEBUG + 'CH' + WHITE, DEBUG + 'K' + WHITE, '   ')))
        checks += 1
    elif black == 2 == checks:
        while True:
            try:
                pc = int(input(f"{pres}President{END} will check number (not index): {DBG_B}")) - 1
                print(END, end='')
                if pc >= c or pc < 0 or pc == pn:
                    raise Exception
            except BaseException as err:
                # print(err)
                print(f"{RED}Wrong syntaxis or too big/small nums{END}")
            else:
                if not input(
                        f"ENTER if number {DBG_B}{pc + 1}{END} is right (it's {DBG_B}[{g[pc]}]{END}), else write something: "):
                    break
        show_only_to_one(f"Color is {get_color(roles[pc])}")
        print(f"Input {BLACK}BLK{END} or {RED}RED{END}")
        cpc = input(f"Color of {g[pc]} {pres}President{END} said: {DBG_B}").upper()
        print(END, end='')  # card_chancellor_placed
        while cpc not in {'BLK', 'RED'}:
            print(f"{RED}WRONG    INPUT{END}")
            cpc = input(f"Color of {DEBUG}{g[pc]}{WHITE} {pres}President{WHITE} said: {DBG_B}").upper()
            print(END, end='')
        if cpc == 'BLK':
            cpc = BLACK + "BLK" + WHITE
        elif cpc == 'RED':
            cpc = RED + "RED" + WHITE
        else:
            print(f"WTH?!!!! {cpc} isn't 'B' or 'R'")
            cpc = DEBUG + "WTH" + WHITE
        logs.append(
            ((g[pn].table(), DEBUG + g[pc].table() + WHITE), (cpc, DEBUG + 'CH' + WHITE, DEBUG + 'K' + WHITE, f'{DEBUG}PLR{WHITE}')))
        checks += 1
    elif black == 3 == checks:
        while True:
            try:
                gulag = int(input(f"{pres}President{END} will place in gulag number (not index): {DBG_B}")) - 1
                print(END, end='')
                if gulag >= c or gulag < 0 or gulag == pn:
                    raise Exception
            except BaseException as err:
                # print(err)
                print(f"{RED}Wrong syntaxis or too big/small nums{END}")
            else:
                if not input(
                        f"ENTER if number {DBG_B}{gulag + 1}{END} is right (it's {DBG_B}[{g[gulag]}]{END}), else write something: "):
                    break
        logs.append(((g[pn].table(), DEBUG + GULAG + g[gulag].table() + BLACK_FONT + WHITE),
                     (DEBUG + 'GUL' + WHITE, DEBUG + 'AG' + WHITE, DEBUG + '!' + WHITE, '   ')))
        g[gulag] = GULAG + DEBUG + g[gulag] + WHITE + BLACK_FONT
        checks += 1
        if gulag == hitler:
            degov()
            Git_caput = True
            break
        else:
            Git_not.add(gulag)
    elif black == 4 == checks:
        temp = pn
        pn = new_gov("President", pres) - 1
        logs.append(((g[temp].table(), g[pn].table()), (DEBUG + 'PLA' + WHITE, DEBUG + 'CE' + WHITE, DEBUG + 'D' + WHITE, '   ')))
        checks += 1
        vnf = True
    elif black == 5 == checks:
        while True:
            try:
                killed = int(input(f"{pres}President{END} will kill number (not index): {DBG_B}")) - 1
                print(END, end='')
                if killed >= c or killed < 0 or killed == pn:
                    raise Exception
            except BaseException as err:
                # print(err)
                print(f"{RED}Wrong syntaxis or too big/small nums{END}")
            else:
                if not input(
                        f"ENTER if number {DBG_B}{killed + 1}{END} is right (it's {DBG_B}[{g[killed]}]{END}), else write something: "):
                    break
        if gulag == killed:
            g[gulag] = g[gulag][10:-10]
            gulag = c
        g[killed] = DEAD + DEBUG + g[killed] + WHITE + BLACK_FONT
        logs.append(((g[pn].table(), g[killed].table()), (DEBUG + 'KIL' + WHITE, DEBUG + 'LE' + WHITE, DEBUG + 'D' + WHITE, '   ')))
        checks += 1
        if killed not in Git_not:
            if killed == hitler:
                degov()
                Git_caput = True
                break
            else:
                Git_not.add(killed)
    # if red >= 3 and molotov_ribbentrop:
    #    input() 
    logs_out()
    if Git_not:
        print("Not Hitlers: ")
        for i in sorted(Git_not):
            print(f'№{i + 1}) {g[i]}')
        print('\n')

logs_out()

with open(full_path, "a+", encoding="UTF-8") as f:
    print(t.strftime("Game  over time:   %d.%m.%y %H:%M:%S"))
    print(t.strftime("Game  over time:   %d.%m.%y %H:%M:%S"), file=f)
    if red >= 5 or Git_caput:
        print(f"{RED}{BOLD}{UNDERLINE}RED    WON!!!{END}")
        print(f"{RED}{BOLD}{UNDERLINE}RED    WON!!!{END}", file=f)
        if Git_caput:
            print(f"{RED}(Hitler caput){WHITE}", file=f)
    elif black >= 6 or Git_cn:
        print(f"{BLACK}{BOLD}{UNDERLINE}BLACK    WON!!!{END}")
        print(f"{BLACK}{BOLD}{UNDERLINE}BLACK    WON!!!{END}", file=f)
        if Git_cn:
            print(f"{BLACK}(Hitler is chancellor){WHITE}", file=f)
    else:
        print(F"{DEBUG}{BOLD}{UNDERLINE}WHAT    THE    HELL?!!!!{END}")
        print(F"{DEBUG}{BOLD}{UNDERLINE}WHAT    THE    HELL?!!!!{END}", file=f)
    print('\n\n\n', file=f)
    out()
