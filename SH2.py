# logging ТГ
import time as t
import os
import sys
import random as rnd
from atexit import register as atexit
from standard_names_SH import *
from standard_functions import color_clear, show_only_to_one, yes_or_no
from HTML_logs import create_HTML_logs, color_of_HTML_roles, Log
from colors import (RED_TEXT as RED,
                    GREEN_TEXT as BLACK,
                    YELLOW_TEXT as YELLOW,
                    BLUE_TEXT as BLUE,
                    PURPLE_TEXT as PURPLE,
                    CYAN_TEXT as CYAN,
                    RED_BACKGROUND as DEAD,
                    YELLOW_BACKGROUND as GULAG,
                    RESET_BACKGROUND as END_BG,
                    RESET_TEXT as END_T, 
                    BOLD, END, UNDERLINE,
                    CRITICAL, WARNING, GOOD,
                    )

INPUT_C = BOLD + PURPLE
ff = __file__
print(ff)
saved = []
NAME_FOR_LOGS = "SH LOG_TEST "  # You can change it
tp = '.html'  # расширение
path = os.path.dirname(ff) + "/LOGS/"
date = t.strftime("%d.%m.%y ")
MAX_NAME_LEN = 15  # You can change it from 10 to infinity
LEN_FOR_TABLET = MAX_NAME_LEN + max(len(CYAN), len(YELLOW)) + len(END_T)
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
special_c = "DeepPink"
special_election = False
skips = 0
logs: list[tuple[tuple[str, str], tuple[str, str, str, str]]] = []
Git_not = set()
g = []  # GAYmers

print(f"If will be error say it to coder (DS: {PURPLE}@fluxxx1k{END})")
normal_logs: list[Log] = []


# Number of players and their names
while True:
    try:
        c = int(input(f"Input number of players: {INPUT_C}"))
        print(END, end='')
        if c < 4 or c > 10:
            raise Exception("Wrong size!")
    except BaseException as err:
        print(f"{RED}Try again, wrong input: {err}{END_T}")
    else:
        if not input(f"If you are sure that here will be {c} gamers press ENTER else write anything: "):
            break
if c == 6:
    print(f"{INPUT_C}5 {RED}RED{PURPLE} cards, 11 {BLACK}BLACK{PURPLE} cards{END}")
    red_start = 5
    black_start = 11
else:
    print(f"{INPUT_C}6 {RED}RED{PURPLE} cards, 11 {BLACK}BLACK{PURPLE} cards{END}")
    red_start = 6
    black_start = 11
deck = ['R'] * red_start + ['B'] * black_start
try:
    os.makedirs(path, exist_ok=True)
    check_logs = os.listdir(path)
except BaseException as err:
    print(f"{CRITICAL}Strange Error: {err}\nLogs won't be created{END}")
else:
    try:
        logs_nums = []
        for i in check_logs:
            if i[:len(NAME_FOR_LOGS) + len(date)] == NAME_FOR_LOGS + date:
                logs_nums.append(i)
        max_log_num = len(logs_nums) + 1
        full_path = path + NAME_FOR_LOGS + date + str(max_log_num) + tp
        while os.path.exists(full_path):
            max_log_num += 1
            print(RED + BOLD + UNDERLINE + full_path +
                  f"    is already exists, trying {CYAN}{max_log_num}{END}")
            full_path = path + NAME_FOR_LOGS + date + str(max_log_num) + tp
        print(f"{GOOD}Logs in: {full_path}{END}")
    except BaseException as err:
        print(f"{CRITICAL}Something went wrong: {err}{END}")
gulag = c
killed = c
roles = [X.HITLER] + [X.BLACK] * (0 if c < 5 else 1 if c < 7 else 2 if c < 9 else 3)
roles.extend([X.RED] * (c - len(roles)))
rnd.shuffle(roles)
hitler = c
stalin = c
try:
    stalin = roles.index(X.STALIN)
except ValueError:
    print("No Sosalin :_((")
except BaseException as err:
    print(f"Can't find {X.STALIN= }: {err}")
try:
    hitler = roles.index(X.HITLER)
except ValueError:
    print(f"{WARNING}WTH? No {X.HITLER} in roles...{END}")
except BaseException as err:
    print(f"Can't find {X.STALIN= }: {err}")

start_time = t.time()
start_time_f = t.strftime("%d.%m.%y %H:%M:%S")
print(start_time_f)
red = black = 0
checks = 1
Git_caput = False
Git_cn = False
f_l = {"OUT", "DEBUG_MODE", "EXIT"}
molotov_ribbentrop = True


def out(count = c, file=sys.stdout):
    for i in range(count):
        print(f"№{i + 1}) {g[i].out()}", file=file)


def coloring(s, sort=True):
    if sort:
        s = sorted(s)
    s1 = ''
    for i in s:
        if i in {"B", "H"}:
            s1 += BLACK + i + END_T
        elif i in {'R', 'S'}:
            s1 += RED + i + END_T
        elif i == 'X':
            s1 += i
        else:
            print(f"{i} should be 'X' or 'R' or 'B'")
    return s1


def naming(s:str) -> str:
    if s in {"R", X.RED}:
        return RED + "RED" + END_T
    if s in {"H", X.HITLER}:
        return BLACK + "HITLER" + END_T
    if s in {"B", "BLACK"}:
        return BLACK + "BLACK" + END_T
    if s in {"S", "STALIN"}:
        return RED + "STALIN" + END_T
    if s in {"M", "MOLOTOV"}:
        return RED + "MOLOTOV" + END_T
    if s in {"REB", "RIBBENTROP"}:
        return BLACK + "RIBBENTROP" + END_T
    if s in {"A", "ANARCHY", "ANARCHIST"}:
        return PURPLE + "ANARCHIST" + END_T
    if s in {"X", "UNKNOWN", "IDK"}:
        return "UNKNOWN"
    return "ERROR"


def dbg(s:str) -> bool:
    s = s.split()
    if len(s) == 3:
        if s[1] == '=':
            s.pop(1)
    if len(s) == 2:
        if s[0] == 'ccp':
            global ccp
            ccp = coloring(s[1])
            print(f"ccp: {ccp}")
            return False
        elif s[0] == 'ccs':
            global ccs
            ccs = coloring(s[1])
            print(f"ccs: {ccs}")
            return False
        elif s[0] == 'cps':
            global cps
            cps = coloring(s[1])
            print(f"cps: {cps}")
            return False
        elif s[0] == 'cpsa':
            global cpsa
            cpsa = coloring(s[1])
            print(f"cpsa: {cpsa}")
            return False
    print(f"{WARNING}Wrong parameters: {s}{END}")
    return True


@atexit
def logs_out():
    create_HTML_logs(path=full_path, logs=normal_logs, players=g, roles=roles)
    logged = 1
    try:
        print(
            f"{END}{UNDERLINE}{BOLD}| {CYAN + 'President' + END_T: <{LEN_FOR_TABLET}} | {YELLOW + 'Chancellor' + END_T: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}")
        for log in logs:
            logged += 1
            print(
                f"{END}{UNDERLINE}{BOLD}| {CYAN + log[0][0] + END_T: <{LEN_FOR_TABLET}} | {YELLOW + log[0][1] + END_T: <{LEN_FOR_TABLET}} | {log[1][0] + END_T: <8} | {log[1][1] + END_T: <7}  | {log[1][2] + END_T: <6}   | {(log[1][3] if len(log[1]) >= 4 else 'XXX') + END_T: <8}  |{END}")
    except BaseException as err:
        print(err)
        try:
            normal_logs.append(
                Log(prs=f"{logged= }", cnc=f"{len(logs)= }", special=err, is_president=False, is_chancellor=False))
        except BaseException as err:
            print(err)
        logged -= 1
        print(
            f"{END}{UNDERLINE}{BOLD}| {CYAN + 'President' + END_T: <{LEN_FOR_TABLET}} | {YELLOW + 'Chancellor' + END_T: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}")
        for log in logs:
            logged -= 1
            if logged:
                print(
                    f"{END}{UNDERLINE}{BOLD}| {CYAN + log[0][0] + END_T: <{LEN_FOR_TABLET}} | {YELLOW + log[0][1] + END_T: <{LEN_FOR_TABLET}} | {log[1][0] + END_T: <8} | {log[1][1] + END_T: <7}  | {log[1][2] + END_T: <6}   | {(log[1][3] if len(log[1]) >= 4 else 'XXX') + END_T: <8}  |{END}")
            else:
                print(*log, sep=f'{END} | ')


def input_cards(text="{RED}Some input: {END_T}", q: int | set[int] = 0, c_p:bool=False, veto=(black >= 5)) -> str:
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
    inp = input(text + END + INPUT_C).strip().upper()
    print(END, end='')
    while len(inp) not in q or (len(letters | set(inp)) > 3 and inp not in letters):
        print(f"{RED}WRONG    INPUT{END}")
        inp = input(PURPLE + "New try: " + END_T + text + END + INPUT_C).strip().upper()
        print(END, end='')
    return inp


def new_gov(gov_type:str=f"GOVERNMENT", color:str=BLUE) -> int:
    while True:
        try:
            gov = int(input(f"{color}{gov_type}{END_T}'s number (not index): {INPUT_C}")) - 1
            print(END, end='')
            if gov >= c or gov < 0 or gov == pn or gov == gulag or gov == killed:
                raise Exception("Wrong number")
        except BaseException as err:
            print(f"{RED}{err}{END}")
        else:
            if not input("ENTER if number is right, else write something: "):
                break
    return gov


def degov() -> None:
    for i in range(c):
        g[i].degov()

    print(f"{PURPLE}  # GOVERNMENT RESET (dbg){END}")
    # out()


def comm(cmd: str) -> bool | None:
    if cmd.upper() in {'LOG', 'LOGS'}:
        logs_out()
    elif cmd == "DEBUG_MODE" or cmd == "DBG":
        while dbg(input(f"{END}DBG: ")):
            pass
    elif cmd == "OUT":
        out()
    elif cmd == '' or name == 'EXIT':
        return False
    return True


def take_random(count:int) -> list[str]:
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
        logs.append(((PURPLE + f'{"DECK":<{MAX_NAME_LEN}}' + END_T, PURPLE + f'{"RESET":<{MAX_NAME_LEN}}' + END_T),
                     (f'{BLACK}BLK{END_T}', f'{BLACK}{str(black_start-black):>2}{END_T}', f'{RED}{red_start-red}{END_T}', f'{RED}RED{END_T}')))
        normal_logs.append(
            Log(special=f"Deck resetting<br>RED: {red_start - red}<br>BLACK: {black_start - black}", is_cards=False))
        deck = ["R"] * (red_start - red) + ["B"] * (black_start - black)
        chosen = rnd.sample(deck, k=count)
    for i in chosen:
        deck.remove(i)
    return chosen


def get_color(x, out_type=''):
    x = color_clear(x)
    for i in [X.BLACK, X.HITLER, X.RIB]:
        if i in x:
            if out_type == "Bot":
                if i == X.HITLER:
                    return X.HTLR
                return X.BLACK
            if out_type == "HTML":
                return black_c
            return BLACK + BOLD + X.BLACK + END
    for i in [X.RED, X.MOLOTOV, X.STALIN]:
        if i in x:
            if out_type == "Bot":
                return X.RED
            if out_type == "HTML":
                return red_c
            return RED + BOLD + X.RED + END
    if X.NRH in x:
        if out_type == "Bot":
            return X.NRH
        if out_type == "HTML":
            return nrh_c
        return BOLD + X.NRH + END
    else:
        if out_type == "Bot":
            print(f"{RED}{BOLD}{UNDERLINE}Bot error, unknown role... Using {PURPLE}ANARCHIST{RED} type...{END}")
            return X.NRH
        if out_type == "HTML":
            return norm_c
        return BOLD + "ERROR, please, show it in IRL" + END


def weighted_random(a, weights):
    return rnd.choices(a, weights, k=1)[0]


class Player:
    base_name = "Player"

    def __init__(self, num, name="RANDOM", role=f"{PURPLE}ANARCHIST{END}"):
        self.gov_pref = ''
        self.gov_suff = ''
        self.purge_pref = ''
        self.purge_suff = ''
        self.num = num
        self.role = role
        self.color = get_color(self.role, out_type='Bot')
        if self.color == X.HITLER:
            self.color = X.BLACK
        self.colored_color = get_color(self.role)
        
        self.prefix = ''
        self.suffix = ''
        if name != "RANDOM":
            self.name = ' '.join(name.split())
        else:
            self.name = Player.base_name + str(num)
        self.tablet_name = f"{self.name: <{MAX_NAME_LEN}}"
        self.dark = 0

    def __repr__(self):
        s = f"{self.name= } ({self.tablet_name= }): {self.role= } (mind_type: {self.color} {self.colored_color= }), {self.dark= }"
        # {len(self.name) == MAX_NAME_LEN = }
        return s

    # def __add__(self, s):
    #     self.suffix += s
    #     return self
    #
    # def __radd__(self, s):
    #     self.prefix += s
    #     return self

    def __str__(self):
        return self.name

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

    # def president(self, card, cnc):
    #def get_color(self):
    #    return self.colored_color

    def free(self, ask=True):
        global gulag
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

    def chosen_gov(self, gov_type):
        if gov_type == X.PRESIDENT:
            self.gov_pref = CYAN
        elif gov_type == X.CHANCELLOR:
            self.gov_pref = YELLOW
        else:
            self.gov_pref = BLUE
            print(f"Unknown government type: {gov_type}")
        self.gov_suff = END_T

    def purge(self, purge_type):
        self.degov()
        if purge_type == X.GULAG:
            self.purge_pref = GULAG
            global gulag
            gulag = self.num
        elif purge_type == X.KILLED:
            global killed
            killed = self.num
            self.purge_pref = DEAD

        self.purge_suff = END_BG

    def president(self, card: str | list[str], cnc: int):
        card = ''.join(sorted(card)).upper()
        show_only_to_one(f"Remember, your role is {naming(self.role)}, color is {self.colored_color}.", hide_len=60)
        card1 = coloring(card.upper())
        print(card1)
        phrase = f"You will say that here: "
        words = input(phrase).strip().upper()
        while len(words) != 3 or not set(words).issubset({'X', "B", "R"}):
            words = input('\x1b[A' + phrase).strip().upper()
        print(f'\x1b[A{phrase}{coloring(words)}')
        phrase1 = f"You will give to chancellor ({g[cnc]}): "
        to_cnc = input(phrase1).strip().upper()
        if to_cnc == "RB":
            to_cnc = "BR"
        while len(to_cnc) != 2 or ("B" + to_cnc != card and to_cnc + "R" != card):
            to_cnc = input('\x1b[A' + phrase1).strip().upper()
        print('\x1b[A\x1b[A\x1b[A' + "#" * len(card)) # ⣿
        print()
        print(phrase1 + '#' * len(to_cnc))
        return words, to_cnc, yes_or_no("Veto? ") if black == 5 else False

    def chancellor(self, card:str, prs, words, veto):
        show_only_to_one(f"Remember, your role is {naming(self.role)}, color is {self.colored_color}.", hide_len=60)
        card1 = coloring(card)
        print(card1)
        phrase = f"You will say that here: "
        words = input(phrase).strip().upper()
        while len(words) != 2 or not set(words).issubset({'X', "B", "R"}):
            words = input('\x1b[A' + phrase).strip().upper()
        print(f'\x1b[A{phrase}{coloring(words)}')
        phrase1 = f"You will place: "
        placed = input(phrase1).strip().upper()
        while len(placed) != 1 or placed not in cards:
            if placed == "VETO" and veto:
                break
            placed = input('\x1b[A' + phrase1).strip().upper()

        print('\x1b[A\x1b[A\x1b[A' + "#" * len(card)) # ⣿
        print()
        if placed == "VETO":
            return words, "X"
        print(phrase1 + coloring(placed))
        return words, placed

    def table(self):
        return self.gov_pref + self.purge_pref + self.prefix + self.tablet_name + self.gov_suff + self.purge_suff + self.suffix

    def out(self):
        return self.gov_pref + self.purge_pref + self.prefix + self.name + self.gov_suff + self.purge_suff + self.suffix



class Bot(Player):
    base_name = "Bot"

    def __init__(self, num="ERR", role=f"{PURPLE}ANARCHIST{END}",
                 name="RANDOM",
                 ):
        super().__init__(num, role, name)
        self.bot_mind = get_color(self.role, out_type='Bot')
        self.risk = rnd.random()
        self.black = []
        if self.bot_mind == X.BLACK:
            for i in range(c):
                if g[i].color == X.BLACK:
                    self.black.append(i)

    def __repr__(self):
        s = super().__repr__()
        s += " "
        s += f"[BOT INFO: {self.bot_mind= }, {self.dark= }, {self.risk= }]"
        return s

    def president(self, card, cnc) -> tuple[str, list[str], bool]:
        card = sorted(card)
        if self.bot_mind == X.HTLR:
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
        if self.bot_mind == X.BLACK:
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
        if self.bot_mind == X.RED:
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
        if self.bot_mind == X.NRH:
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
        if self.bot_mind == X.RED:
            if "R" in card:
                return "XX", "R"
            elif veto:
                return "XX", "X"
            else:
                return "XX", 'B'
        if self.bot_mind == X.HTLR:
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
        if self.bot_mind == X.BLACK:
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
            if self.bot_mind != X.NRH:
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
#        if self.bot_mind == X.RED:
#            return x.name, x.colored_color
#        if self.bot_mind = X.BLACK:
#
#    def check_cards(self,  card):
#        print(coloring("BBB"))
for i in range(c):
    name = input(f"GAYmer №{i + 1}) {INPUT_C}")
    print(END, end='')
    while len(name) > MAX_NAME_LEN or name == '' or name in g:
        print(f"{RED}Length of name should be 1-{MAX_NAME_LEN} symbols!{END}")
        name = input(f"{RED}New attempt:{END} GAYmer №{i + 1}) {INPUT_C}")
        print(END, end='')

    g.append(Player(num=i, name=name, role=roles[i]))
err = []
while True:
    try:
        err = list(map(int, input(f"Print numbers of mistakes: {INPUT_C}").split()))
        print(END, end='')
        for i in err:
            if i > c or i < 1:
                raise Exception
    except BaseException as err:
        print(f"{RED}{err}{END}")
    else:
        break
for i in err:
    name = input(f"{PURPLE}Fixing names:{END} GAYmer №{i}) {INPUT_C}").strip()
    print(END, end='')
    while len(name) > MAX_NAME_LEN or name == '' or name in g:
        print(f"{RED}Length of name should be 1-{MAX_NAME_LEN} symbols!{END}")
        name = input(f"{RED}New try:{END} GAYmer №{i}) {INPUT_C}").strip()
        print(END, end='')
    g[i - 1].name = name
print(*list(map(repr, g)), sep='\n')

for i in range(c):
    print(f"{PURPLE}{INPUT_C}[{g[i]}]{END}, come here to get your role!")
    show_only_to_one(f"Your role is: {INPUT_C}{naming(roles[i])}{END}", 25)

while True:
    try:
        pn = int(input(f"{CYAN}President{END}'s number (not index): {INPUT_C}")) - 1
        print(END, end='')
        if pn >= c or pn < 0:
            raise Exception
    except BaseException as err:
        print(f"{RED}{err}{END}")
    else:
        if not input("ENTER if number is right, else write something: "):
            break
pn -= 1
pnc = pn
while red < 5 and black < 6 and not Git_caput and not Git_cn:
    if pnc != pn:
        if special_election:
            print(f"{PURPLE}{pnc = } != {pn = } => Внеоф{END_T}")
        else:
            # print(f"{PURPLE}WTF?!! (Line 160)")
            print(f"{PURPLE}{pnc = } != {pn = } but {special_election = }{END_T}")
            pn = pnc
    if skips > 2:
        if yes_or_no(f"Anarchy? (Skips: {skips}): "):
            if saved:
                logs.append(((f"{PURPLE + 'SHUFFLED' + END_T: <{LEN_FOR_TABLET}}",
                          f"{PURPLE + 'CARDS' + END_T: <{LEN_FOR_TABLET}}"), ('   ', '  ', ' ', '   ')))
                normal_logs.append(Log(special="Cards was shuffled!"))
                ccp = rnd.sample(saved, k=1)[0]
            else:
                ccp = take_random(1)[0]
            logs.append(((f"{PURPLE + 'ANARCHY' + END_T: <{LEN_FOR_TABLET}}",
                          f"{PURPLE + 'ANARCHY' + END_T: <{LEN_FOR_TABLET}}"), ('   ', '  ', coloring(ccp), '   ')))
            normal_logs.append(Log(c_cnc_placed=ccp, special="Anarchy"))
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
                logs.append(((f"{PURPLE + 'ANARCHY' + END_T: <{LEN_FOR_TABLET}}", g[gulag].table()),
                             (f'{PURPLE}FRE{END_T}', f'{PURPLE}E!{END_T}', f'{PURPLE}!{END_T}', '   ')))
                print(f"{PURPLE}{g[gulag]} was de-Gulag-ed{END_T}")
                normal_logs.append(Log(special=f"Anarchy, {g[gulag]} freed"))
                g[gulag].free()
                gulag = c
            logs_out()
    pn = (pn + 1) % c
    if pn == gulag:
        print(f"{PURPLE}President can't be in gulag, next{END_T}")
        pn = (pn + 1) % c
    if pn == killed:
        print(f"{PURPLE}President can't be dead, next{END_T}")
        pn = (pn + 1) % c
    if pn == gulag:
        print(f"{PURPLE}President can't be in gulag, next{END_T}")
        pn = (pn + 1) % c
    g[pn].chosen_gov(X.PRESIDENT)
    out()
    if not special_election:
        pnc = pn
    else:
        # if pnc == pn:
        #    pnc =
        special_election = False
    if yes_or_no(f"Skip? (Skips: {skips}): "):
        skips += 1
        degov()
        print("\n\n\n")
        continue
    else:
        skips = 0

    cn = new_gov("Chancellor", YELLOW)
    if black >= 3 and cn not in Git_not:
        if c == stalin:
            if cn == hitler:
                degov()
                logs.append(((g[pn].table(), g[cn].table()),
                             (f'{BLACK}HIT{END_T}', f'{BLACK}LE{END_T}', f'{BLACK}R{END_T}', '   ')))
                normal_logs.append(Log(prs=g[pn], cnc=g[cn], special="Hitler is chancellor!"))
                Git_cn = True
                break
            else:
                Git_not.add(cn)
        else:
            if hitler == cn:
                if yes_or_no(f"Is {g[cn].name} hitler "):
                    degov()
                    logs.append(((g[pn].table(), g[cn].table()),
                                 (f'{BLACK}HIT{END_T}', f'{BLACK}vs{END_T}', f'{BLACK}S{END_T}', 'TAL')))
                    normal_logs.append(
                        Log(prs=g[pn], cnc=g[cn], special="Hitler is chancellor!<br>But Stalin is president!"))
                    Git_caput = True
                    break
            else:
                yes_or_no(f"Is {g[cn].name} hitler? ", yes=set())
    g[cn].chosen_gov(X.CHANCELLOR)
    out()
    cards = take_random(3)
    cps, cards, veto = g[pn].president(cards, cn)
    ccs, ccp = g[cn].chancellor(cards, pn, cps, veto)
    cpsa = input_cards(f"Cards {CYAN}president{END_T} ({g[pn]}) said after chancellor: ", q={3, 0})
    temp = input(f'Command: {INPUT_C}').upper()
    print(END, end='')
    while comm(temp):
        temp = input(f'Command (new try): {INPUT_C}').upper()
        print(END, end='')
    if ccp == 'B' or ccp == BLACK + "B" + END_T:
        black += 1
    elif ccp == 'R' or ccp == RED + "R" + END_T:
        red += 1
    elif ccp == 'P' or ccp == PURPLE + "P" + END_T:
        red += 1
        black += 1
    elif (ccp == 'VETO' or ccp == "X") and black >= 5:
        print(f"{PURPLE}Passing cuz VETO{END_T}")
        ccp = "V"
    else:
        print(f"WTH?!!!! {ccp} isn't 'B' or 'R'")
        ccp = input_cards("New (last) try to input cards (debug version):", 1, c_p = True)
    if not cpsa:
        cpsa = cps
    
    cps = coloring(cps)
    ccs = coloring(ccs)
    if ccp != 'V':
        ccp = coloring(ccp)
        normal_logs.append(Log(prs=g[pn], cnc=g[cn], c_prs_said=cps, c_cnc_said=ccs, c_cnc_placed=ccp, c_prs_said_after=cpsa))
    else:
        normal_logs.append(Log(prs=g[pn], cnc=g[cn], c_prs_said=cps, c_cnc_said=ccs, c_cnc_placed="VETO", c_prs_said_after=cpsa, special="VETO"))
        ccp = PURPLE + "V" + END_T
    cpsa = coloring(cpsa)
    degov()
    print("\n\n\n")

    logs.append(((g[pn].table(), g[cn].table()), (cps, ccs, ccp, cpsa)))
    if black == 1 == checks:
        saved = take_random(3)
        show_only_to_one(coloring(saved))
        cpsc = input_cards(f"Cards {CYAN}president{END} said after checking: ", q=3)
        cpsc = coloring(cpsc)
        logs.append(((g[pn].table(), f"{PURPLE + 'CARD CHECK' + END_T: <{LEN_FOR_TABLET}}"),
                     (cpsc, PURPLE + 'CH' + END_T, PURPLE + 'K' + END_T, '   ')))
        normal_logs.append(Log(prs=g[pn], c_prs_said=cpsc, special="Card check"))
        checks += 1
    elif black == 2 == checks:
        while True:
            try:
                pc = int(input(f"{CYAN}President{END} will check number (not index): {INPUT_C}")) - 1
                print(END, end='')
                if pc >= c or pc < 0 or pc == pn:
                    raise Exception
            except BaseException as err:
                print(f"{RED}{err}{END}")
            else:
                if not input(
                        f"ENTER if number {INPUT_C}{pc + 1}{END} is right (it's {INPUT_C}[{g[pc]}]{END}), else write something: "):
                    break
        show_only_to_one(f"Color is {get_color(roles[pc])}")
        print(f"Input {BLACK}BLK{END} or {RED}RED{END}")
        cpc = input(f"Color of {g[pc]} {CYAN}President{END} said: {INPUT_C}").upper()
        print(END, end='')  # card_chancellor_placed
        while cpc not in {X.BLACK, X.RED, X.NRH}:
            print(f"{RED}WRONG    INPUT{END}")
            cpc = input(f"Color of {PURPLE}{g[pc]}{END_T} {CYAN}President{END_T} said: {INPUT_C}").upper()
            print(END, end='')
        if cpc == X.BLACK:
            cpc1 = BLACK + "BLK" + END_T
        elif cpc == X.RED:
            cpc1 = RED + "RED" + END_T
        elif cpc == X.NRH:
            cpc1 = PURPLE + "NRH" + END_T
        else:
            print(f"WTH?!!!! {cpc} isn't '{X.BLACK}' or '{X.RED}'")
            cpc1 = PURPLE + "WTH" + END_T
        logs.append(
            ((g[pn].table(), PURPLE + g[pc].table() + END_T),
             (cpc1, PURPLE + 'CH' + END_T, PURPLE + 'K' + END_T, f'{PURPLE}PLR{END_T}')))
        normal_logs.append(
            Log(prs=g[pn], cnc=g[cn],
                special=f"Color of <font color='{purple_c}'>{g[cn]}</font> <font color='{pr_c}'>{g[pn]}</font> said is <font color='{color_of_HTML_roles(cpc)}'>{cpc}</font>",
                is_chancellor=False))
        checks += 1
    elif black == 3 == checks:
        while True:
            try:
                gulag = int(input(f"{CYAN}President{END} will place in gulag number (not index): {INPUT_C}")) - 1
                print(END, end='')
                if gulag >= c or gulag < 0 or gulag == pn:
                    raise Exception
            except BaseException as err:
                print(f"{RED}{err}{END}")
            else:
                if not input(
                        f"ENTER if number {INPUT_C}{gulag + 1}{END} is right (it's {INPUT_C}[{g[gulag]}]{END}), else write something: "):
                    break
        logs.append(((g[pn].table(), PURPLE + GULAG + g[gulag].table() + END_BG + END_T),
                     (PURPLE + 'GUL' + END_T, PURPLE + 'AG' + END_T, PURPLE + '!' + END_T, '   ')))
        normal_logs.append(Log(g[pn], g[gulag], special="In gulag", is_cards=False, is_chancellor=False))
        g[gulag].purge(X.GULAG)
        checks += 1
        if gulag == hitler:
            degov()
            Git_caput = True
            break
        else:
            Git_not.add(gulag)
    elif black == 4 == checks:
        temp = pn
        pn = new_gov("President", CYAN) - 1
        logs.append(((g[temp].table(), g[pn + 1].table()),
                     (PURPLE + 'PLA' + END_T, PURPLE + 'CE' + END_T, PURPLE + 'D' + END_T, '   ')))
        normal_logs.append(Log(g[temp], g[pn + 1], special="Special placing", is_chancellor=False))
        checks += 1
        special_election = True
    elif black == 5 == checks:
        while True:
            try:
                killed = int(input(f"{CYAN}President{END} will kill number (not index): {INPUT_C}")) - 1
                print(END, end='')
                if killed >= c or killed < 0:
                    raise ValueError("Wrong number")
                elif killed == pn:
                    raise ValueError("No suicide!!")
            except BaseException as err:
                print(f"{RED}{err}{END}")
            else:
                if not input(
                        f"ENTER if number {INPUT_C}{killed + 1}{END} is right (it's {INPUT_C}[{g[killed]}]{END}), else write something: "):
                    break
        if gulag == killed:
            gulag = c
        g[killed].purge(X.KILLED)
        logs.append(((g[pn].table(), g[killed].table()),
                     (PURPLE + 'KIL' + END_T, PURPLE + 'LE' + END_T, PURPLE + 'D' + END_T, '   ')))
        normal_logs.append(Log(g[pn], g[killed], special=f"Killed", is_chancellor=False))
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
try:
    with open(full_path, "a+", encoding="UTF-8") as f:
        end_time_f = t.strftime("%d.%m.%y %H:%M:%S")
        end_time = t.time()
        print("Game over time: " + end_time_f)
        print("Game start time: " + start_time_f, file=f)
        print("Game over time: " + end_time_f, file=f)

        if red >= 5 or Git_caput:
            print(f"{RED}{BOLD}{UNDERLINE}RED    WON!!!{END}")
            print(f"{RED}{BOLD}{UNDERLINE}RED    WON!!!{END}", file=f)
            if Git_caput:
                print(f"{RED}(Hitler caput){END_T}", file=f)
        elif black >= 6 or Git_cn:
            print(f"{BLACK}{BOLD}{UNDERLINE}BLACK    WON!!!{END}")
            print(f"{BLACK}{BOLD}{UNDERLINE}BLACK    WON!!!{END}", file=f)
            if Git_cn:
                print(f"{BLACK}(Hitler is chancellor){END_T}", file=f)
        else:
            print(F"{PURPLE}{BOLD}{UNDERLINE}WHAT    THE    HELL?!!!!{END}")
            print(F"{PURPLE}{BOLD}{UNDERLINE}WHAT    THE    HELL?!!!!{END}", file=f)
        print('\n\n\n', file=f)
        out()
except FileNotFoundError:
    print("Can't open file")
except BaseException as err:
    print(f"{RED}{BOLD}{UNDERLINE}Something went wrong: {err}{END}")