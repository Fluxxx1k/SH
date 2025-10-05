# logging ТГ
import time as t
import os
import sys
import random as rnd
import platform
release = platform.release()

ff = __file__
print(ff)
LIGHT_BLUE = pres = '\033[36m'  # WHITE_BLUE
YELLOW = canc = '\033[33m'  # YELLOW
BLUE = BASE = '\033[34m'  # BLUE
PURPLE = DEBUG = '\033[35m'  # PURPLE
RED = '\033[31m'
BLACK = '\033[32m'  # GREEN
END = '\033[0m'
BOLD = '\033[1m' + DEBUG
BOLD_2 = '\033[1m'
UNDERLINE = '\033[4m'
GREY = '\033[37m'
saved = []
DEAD = '\033[41m'  # RED_FONT
GULAG = '\033[43m'  # YELLOW_FONT
BLACK_FONT = '\033[40m'
NAME_FOR_LOGS = "SH LOG_TEST "  # You can change it
tp = '.txt'  # расширение
path = os.path.dirname(ff) + '/'
date = t.strftime("%d.%m.%y ")
MAX_NAME_LEN = 15  # You can change it from 10 to infinity
if 'android' in release.lower() or 'lineageos' in release.lower():
    WHITE = '\033[37m'
    print(f"{YELLOW}Launched on Android{END}")
else:
    WHITE = '\033[38m'
LEN_FOR_TABLET = MAX_NAME_LEN + len(pres + WHITE)

print(f"If 1 of this colors is blue say it to coder (DS: {PURPLE}@fluxxx1k{END}): {BLUE}{WHITE}ABC{BLUE}{GREY}ABC{END}")

# Number of players and their names
while True:
    try:
        c = int(input(f"Input number of players: {BOLD}")); print(END, end='')
        if c < 4 or c > 10:
            raise Exception
    except:
        print(f"{RED}Try again, wrong input{WHITE}")
    else:
        if not input(f"If you are sure that here will be {c} gamers press ENTER else write anything: "):
            break
if c == 6:
    print(f"{BOLD}5 {RED}RED{DEBUG} cards, 11 {BLACK}BLACK{DEBUG} cards{END}")
    red_start = 5
    black_start = 11
else:
    print(f"{BOLD}6 {RED}RED{DEBUG} cards, 11 {BLACK}BLACK{DEBUG} cards{END}")
    red_start = 6
    black_start = 11
deck = ['R']*red_start + ['B']*black_start
check_logs = os.listdir(path)
logs_nums = []


for i in check_logs:
    if i[:len(NAME_FOR_LOGS) + len(date)] == NAME_FOR_LOGS + date:
        logs_nums.append(i)
max_log_num = len(logs_nums) + 1
full_path = path + NAME_FOR_LOGS + date + str(max_log_num) + tp
while os.path.exists(full_path):
    max_log_num += 1
    print(RED+BOLD_2+UNDERLINE+path + NAME_FOR_LOGS + date + str(max_log_num) + tp +
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
molotov_rebbentrop = True


def out(file=sys.stdout):
    for i in range(c):
        print(f"№{i+1}) {g[i]}", file=file)


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

#def add_2_logs(x, y, a, b, c):
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



def logs_out():
    r = ''
    with open(full_path, 'r', encoding='UTF-8') as f:
        r = f.read()
    r = r[:r.find('-'*20)] + '\n'
    log = 1
    try:
        f = open(full_path, "w+", encoding="UTF-8")
        print(r, file=f)
        print('-'*20, file=f)
        print(f"{END}{UNDERLINE}{BOLD_2}| {pres+'President'+WHITE: <{LEN_FOR_TABLET}} | {canc+'Cancler'+WHITE: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}", file=f)
        print(f"{END}{UNDERLINE}{BOLD_2}| {pres+'President'+WHITE: <{LEN_FOR_TABLET}} | {canc+'Cancler'+WHITE: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}")
        for i in logs:
            log += 1
            print(f"{END}{UNDERLINE}{BOLD_2}| {pres + i[0][0] + WHITE: <{LEN_FOR_TABLET}} | {canc + i[0][1] + WHITE: <{LEN_FOR_TABLET}} | {i[1][0]+WHITE: <8} | {i[1][1]+WHITE: <7}  | {i[1][2]+WHITE: <6}   | {(i[1][3] if len(i[1]) >= 4 else 'XXX')+WHITE: <8}  |{END}", file=f)
            print(f"{END}{UNDERLINE}{BOLD_2}| {pres + i[0][0] + WHITE: <{LEN_FOR_TABLET}} | {canc + i[0][1] + WHITE: <{LEN_FOR_TABLET}} | {i[1][0]+WHITE: <8} | {i[1][1]+WHITE: <7}  | {i[1][2]+WHITE: <6}   | {(i[1][3] if len(i[1]) >= 4 else 'XXX')+WHITE: <8}  |{END}")
    except BaseException as r:
        f = open(full_path, "w+", encoding="UTF-8")
        print(r, file=f)
        print('-'*20, file=f)
        log -=1
        print(f"{END}{UNDERLINE}{BOLD_2}| {pres+'President'+WHITE: <{LEN_FOR_TABLET}} | {canc+'Cancler'+WHITE: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}", file=f)
        print(f"{END}{UNDERLINE}{BOLD_2}| {pres+'President'+WHITE: <{LEN_FOR_TABLET}} | {canc+'Cancler'+WHITE: <{LEN_FOR_TABLET}} | CPS | CCS | CCP | CPSA |{END}")
        for i in logs:
            log -= 1
            if log:
                print(f"{END}{UNDERLINE}{BOLD_2}| {pres + i[0][0] + WHITE: <{LEN_FOR_TABLET}} | {canc + i[0][1] + WHITE: <{LEN_FOR_TABLET}} | {i[1][0]+WHITE: <8} | {i[1][1]+WHITE: <7}  | {i[1][2]+WHITE: <6}   | {(i[1][3] if len(i[1]) >= 4 else 'XXX')+WHITE: <8}  |{END}", file=f)
                print(f"{END}{UNDERLINE}{BOLD_2}| {pres + i[0][0] + WHITE: <{LEN_FOR_TABLET}} | {canc + i[0][1] + WHITE: <{LEN_FOR_TABLET}} | {i[1][0]+WHITE: <8} | {i[1][1]+WHITE: <7}  | {i[1][2]+WHITE: <6}   | {(i[1][3] if len(i[1]) >= 4 else 'XXX')+WHITE: <8}  |{END}")
            else:
                print(*i, sep='{END} | ', file=f)
                print(*i, sep='{END} | ')
    finally:
        f.close()

def input_cards(text = "{RED}Some input: {WHITE}", q: int | set[int] = 0, c_p = False, veto=(black>=5)) -> str:
    """
    c_p - cancler placing, don't laugh
    """
    if not veto is True and not veto is False:
        print(f"{RED}{BOLD_2}{UNDERLINE}{veto = } | it's not good!{END}")
        veto = True
    letters = {'X', 'R', 'B'}
    if q == 0:  # quality didn't change
        print("{RED}{BOLD_2}{UNDERLINE}Input lenght is {q = }, it will be 1-3 now")
        q = {1, 2, 3}
    elif not isinstance(q, set):
        q = {q}
    if c_p and not veto:  # cancler should place card if it wasn't veto
        letters -= {'X'}
    if c_p:  # if president was skipped in game, but not in code 
        letters.add("SKIP")
    inp = input(text+END+BOLD).strip().upper(); print(END, end='')
    while len(inp) not in q or (len(letters | set(inp)) > 3 and inp not in letters):
        print(f"{RED}WRONG    INPUT{END}")
        inp = input(DEBUG+"New try: " + WHITE +    text+END+BOLD).strip().upper(); print(END, end='')
    return inp



def new_gov(gov_type=f"GOVERMENT", color=BASE):
    gov = 0
    while True:
        try:
            gov = int(input(f"{color}{gov_type}{WHITE}'s number (not index): {BOLD}")) - 1; print(END, end='')
            if gov >= c or gov < 0 or gov == pn or gov == gulag or gov == killed:
                raise Exception
        except:
            print(f"{RED}Wrong syntaxis or too big/small nums{END}")
        else:
            if not input("ENTER if number is right, else write something: "):
                break
    g[gov] = color  + g[gov] + WHITE
    out()
    return gov


def degov():
    for i in range(3):
        for i in range(c):
            if g[i][:5] in {pres, canc}:
                g[i] = g[i][5:-5]

    print(f"{DEBUG}  # GOVERMENT RESETED (dbg){END}")
    #out()


def comm(name):
    if name.upper() in {"H", "HELP"}:
        print(*sorted(f_l), sep=', ')
        print(f"{RED}May be mistakes{END}")
    if name.upper() == {'LOG', 'LOGS'}:
        logs_out()
    elif name == "DEBUG_MODE" or name == "DBG":
        print(f"{END}{BOLD}To exit from debug mode write \"exit\"\n{END}{RED}{BOLD_2}DO    NOT    USE{END}{RED}    \"exit()\"    OR    \"Ctrl + D\"{END}")
        try:
            breakpoint()
        except BaseException as r:
            print(r)
        print(END, end='')
    elif name == "OUT":
        out()
    elif name == '' or name == 'EXIT':
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
            print(f"{END}\x1b[A\x1b[A" +    "⣿" * hide_len)
            print()


def take_random(c):
    global saved
    if saved:
        x = saved.copy()
        saved = []
        return x
    global deck
    try:
        chosen = rnd.sample(deck, k=c)
    except ValueError:
        print("DECK RESET")
        logs.append(((DEBUG+f'{"DECK":<{MAX_NAME_LEN}}'+WHITE, DEBUG+f'{"RESET":<{MAX_NAME_LEN}}'+WHITE),('   ', '  ', ' ', '   ')))
        deck = ["R"]*(red_start - red) + ["B"] * (black_start - black)
        chosen = rnd.sample(deck, k=c)
    for i in chosen:
        deck.remove(i)
    rnd.shuffle(chosen)
    return chosen


def yes_or_no(text='Input for something (If you see it, you should understand what shoud be asked): ', yes:set|frozenset = frozenset({'y', 'Y', 'Y|y', 'yes', 'Yes', 'YES'}), no:set|frozenset = frozenset({'N', 'n', 'N|n', 'no', "No", "NO"})):
    inp = input(text + ' ').strip()
    while inp not in yes and inp not in no:
        inp=input('\x1b[A' + f"{DEBUG}{text} New try: {END}").strip()
    if inp in yes:
        return True
    if inp in no:
        return False
    print(f"WTF: {inp}")
    return False


def get_color(x, out_type=''):
    for i in ["BLACK", "HITLER", "REBBENTROP"]:
        if i in x:
            if out_type == "Bot":
#                if i == "HITLER":
#                    return "HTLR"
                return "BLK"
            return BLACK+BOLD_2+"BLACK"+END
    for i in ["RED", "MOLOTOV", "STALIN"]:
        if i in x:
            if out_type == "Bot" :
                return "RED"
            return RED+BOLD_2+"RED"+END
    if "ANARCHYST" in x:
        if out_type == "Bot" :
                return "NRH"
        return BOLD+"ANARCHYST"+END
    else:
        if out_type == "Bot" :
                print(f"{RED}{BOLD_2}{UNDERLINE}Bot ERR, unknown role... Using {BOLD}ANARHY{RED} type...{END}")
                return "NRH"
        return BOLD_2+"ERROR, please, show it in IRL" + END
roles = [f"{BLACK}HITLER{END}"] + [f"{BLACK}BLACK{END}" * (1 if c < 7 else 2)]
roles.extend([f"{RED}RED{END}"] * (c - len(roles)))
rnd.shuffle(roles)
hitler = roles.index(f"{BLACK}HITLER{END}")
stalin = c
try:
    stalin = roles.index(f"{RED}STALIN{END}")
except:
    print("No Sosalin :_((")
class Player:
    base_name = "Player"
    def __init__(self, num="ERR", role = f"{DEBUG}ANARCHYST{END}",
    name = "RANDOM",
    ):
        self.role = role
        self.color = get_color(self.role)
        if name != "RANDOM":
            self.name = ' '.join(name.split())
        else:
            if num == "ERR" or len(str(num)) > len(Player.base_name):
                self.name = Player.base_name + str(rnd.random())[2:MAX_NAME_LEN-7]
            else:
                self.name = Player.base_name + str(num)
        self.tablet_name = str(num) + self.name #f"{self.name: <{LEN_FOR_TABLET}}"
        self.dark = 0

    def __repr__(self):
        s = f"{self.name= } ({self.tablet_name= }): {self.role= } (mind_type: {self.color= }), {self.dark= }"
        #{len(self.name) == MAX_NAME_LEN = }
        return s

    #def __str__(self):
#        return self.name

    def __eq__(self, other):
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



class Bot(Player):
    base_name= "Bot"
    def __init__(self, num="ERR", role = f"{DEBUG}ANARCHYST{END}",
    name = "RANDOM",
    ):
        super().__init__(num, role, name)
        self.bot_mind = get_color(self.role, out_type='Bot')

    def __repr__(self):
        s = super().__repr__()
        s += " "
        s += f"[BOT INFO: {self.bot_mind= }, {self.dark= }]"
        return s

pn = c + 1
#pn = int(input(f"{pres}President{END}'s number (not index): ")) - 1
vnf = False
skips = 0
logs = []
gulag = c
killed = c
Git_not = set()
g = []  # GAYmers
for i in range(c):
    temp = input(f"GAYmer №{i + 1}) {BOLD}"); print(END, end='')
    while len(temp) > MAX_NAME_LEN or temp == '':
        print(f"{RED}Lenght of name should be 1-{MAX_NAME_LEN} symbols!{END}")
        temp = input(f"{RED}New attempt:{END} GAYmer №{i + 1}) {BOLD}"); print(END, end='')
    g.append(temp)
err = []
while True:
    try:
        err = list(map(int, input(f"Print numbers of mistakes: {BOLD}").split())); print(END, end='')
        for i in err:
            if i > c or i < 1:
                raise Exception
    except:
        print(f"{RED}Wrong syntax or too big nums{END}")
    else:
        break
for i in err:
    temp = input(f"{DEBUG}Fixing names:{END} GAYmer №{i}) {BOLD}").strip(); print(END, end='')
    while len(temp) > MAX_NAME_LEN or temp == '':
        print(f"{RED}Lenght of name should be 1-{MAX_NAME_LEN} symbols!{END}")
        temp = input(f"{RED}New try:{END} GAYmer №{i}) {BOLD}").strip(); print(END, end='')
    g[i -1] = temp

for i in range(c):
    g[i] = f"{g[i]: <{MAX_NAME_LEN}}"    # Changing lenght of name

while True:
    try:
        pn = int(input(f"{pres}President{END}'s number (not index): {BOLD}")) - 1; print(END, end='')
        if pn >= c or pn < 0:
            raise Exception
    except BaseException as r:
        #print(r)
        print(f"{RED}Wrong syntaxis or too big/small nums{END}")
    else:
        if not input("ENTER if number is right, else write something: "):
            break
pn -=1
pnc = pn


with open(full_path, 'a+', encoding='UTF-8') as f:
    print(start_time, file=f)

with open(full_path, 'a+', encoding="UTF-8") as f:
    for i in range(c):
        print(f"{PURPLE}{BOLD}[{g[i]}]{END}, come here to get your role!")
        show_only_to_one(f"Your role is: {BOLD}{roles[i]}{END}", 25)
        print(f"№{i + 1} ({g[i]}) was {roles[i]}", file=f)

while red < 5 and black < 6 and not Git_caput and not Git_cn:
    if pnc != pn:
        if vnf:
            print(f"{DEBUG}{pnc = } != {pn = } => Внеоф{WHITE}")
        else:
            #print(f"{DEBUG}WTF?!! (Line 160)")
            print(f"{DEBUG}{pnc = } != {pn = } but {vnf = }{WHITE}")
            pn = pnc
    if skips > 2:
        if yes_or_no(f"Anarhy? (Skips: {skips}): "):
            ccp = take_random(1)[0]
            logs.append(((f"{DEBUG+'SHUFFLED'+WHITE: <{LEN_FOR_TABLET}}",f"{DEBUG+'CARDS'+WHITE: <{LEN_FOR_TABLET}}"),('   ','  ',' ', '   ')))
            logs.append(((f"{DEBUG+'ANARHY'+WHITE: <{LEN_FOR_TABLET}}", f"{DEBUG+'ANARHY'+WHITE: <{LEN_FOR_TABLET}}"),('   ', '  ', coloring(ccp), '   ')))
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
                logs.append(((f"{DEBUG+'ANARHY'+WHITE: <{LEN_FOR_TABLET}}", g[gulag]),(f'{DEBUG}FRE{WHITE}', f'{DEBUG}E!{WHITE}', f'{DEBUG}!{WHITE}', '   ')))
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
    g[pn] = pres + g[pn] + WHITE
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

    cn = new_gov("Cancler", canc)
    if black >=3 and cn not in Git_not:
        if cn == hitler:
            if pn != stalin:
                degov()
                logs.append(((g[pn], g[cn]), (f'{BLACK}HIT{WHITE}', f'{BLACK}LE{WHITE}', f'{BLACK}R{WHITE}', '   ')))
                Git_cn = True
            else:
                degov()
                logs.append(((g[pn], g[cn]), (f'{BLACK}HIT{WHITE}', f'{BLACK}vs{WHITE}', f'{BLACK}S{WHITE}', 'TAL')))
                Git_caput = True
            break
        else:
            Git_not.add(cn)
    #show_only_to_one(coloring(take_random(3)))
    show_only_to_one(coloring(cards:=take_random(3), sort=False))
    cps = input_cards(f"Cards {pres}president{WHITE} ({g[pn]}) said: ", q=3)
    cps = coloring(cps)
    cpd = input(f"Say NUMBER (1-3) of card to drop (in order that you saw) (cancler won't get it): ")
    while not cpd.isdigit() or (1 > int(cpd) or 3 < int(cpd)):
        cpd = input(f"{DEBUG}New try: {END}")
    cards.pop(int(cpd) - 1)

    show_only_to_one(coloring(cards))
    ccs = input_cards(f"Cards {canc}cancler{END} ({g[cn]}) said: ", q=2)
    ccs = coloring(ccs)
    ccp = input_cards(f"Card {canc}cancler{END} ({g[cn]}) placed: ", q=1, c_p=True)
    while ccp not in cards:
        ccp = input_cards(f"\x1b[ACard {canc}cancler{END} ({g[cn]}) placed: ", q=1, c_p=True)
    cpsa = input_cards(f"Cards {pres}president{WHITE} ({g[pn]}) said after cancler: ", q={3, 0})
    if cpsa:
        cpsa = coloring(cpsa)
    else:
        cpsa = cps

    temp = input(f'Comand: {BOLD}').upper(); print(END, end='')
    while not comm(temp):
        #print(f"{RED}Wrong syntaxis{END}")
        temp = input(f'Comand (new try): {BOLD}').upper(); print(END, end='')
    if  ccp == 'B' or ccp == BLACK + "B" + WHITE:
        black += 1
    elif ccp == 'R' or ccp == RED + "R" + WHITE:
        red += 1
    elif ccp == 'VETO' and black >= 5:
        print(f"{DEBUG}Passing cuz VETO{WHITE}")
        degov()
        continue
    else:
        print(f"WTH?!!!! {ccp} isn't 'B' or 'R'")
        ccp = 'X'
    ccp = coloring(ccp)

    degov()
    print("\n\n\n")

    logs.append(((g[pn], g[cn]), (cps, ccs, ccp, cpsa)))
    if black == 1 ==   checks:
        saved = take_random(3)
        show_only_to_one(coloring(saved))
        cpsc = input_cards(f"Cards {pres}president{END} said after checking: ", q=3)
        cpsc = coloring(cpsc)
        logs.append(((g[pn], f"{DEBUG+'CARD CHECK'+WHITE: <{LEN_FOR_TABLET}}"), (cpsc, DEBUG + 'CH' + WHITE, DEBUG + 'K' + WHITE, '   ')))
        checks += 1
    elif black == 2  ==    checks:
        while True:
            try:
                pc = int(input(f"{pres}President{END} will check number (not index): {BOLD}")) - 1; print(END, end='')
                if pc >= c or pc < 0 or pc == pn:
                    raise Exception
            except BaseException as r:
                #print(r)
                print(f"{RED}Wrong syntaxis or too big/small nums{END}")
            else:
                if not input(f"ENTER if number {BOLD}{pc+1}{END} is right (it's {BOLD}[{g[pc]}]{END}), else write something: "):
                    break
        show_only_to_one(f"Color is {get_color(roles[pc])}")
        print(f"Input {BLACK}BLK{END} or {RED}RED{END}")
        cpc = input(f"Color of {g[pc]} {pres}President{END} said: {BOLD}").upper(); print(END, end='')  # card_cancler_placed
        while cpc not in {'BLK', 'RED'}:
            print(f"{RED}WRONG    INPUT{END}")
            cpc = input(f"Color of {DEBUG}{g[pc]}{WHITE} {pres}President{WHITE} said: {BOLD}").upper(); print(END, end='')
        if cpc == 'BLK':
            cpc = BLACK + "BLK" + WHITE
        elif cpc == 'RED':
            cpc = RED + "RED" + WHITE
        else:
            print(f"WTH?!!!! {cpc} isn't 'B' or 'R'")
            cpc = DEBUG +"WTH" + WHITE
        logs.append(((g[pn], DEBUG + g[pc] + WHITE), (cpc, DEBUG + 'CH' + WHITE, DEBUG + 'K' + WHITE, f'{DEBUG}PLR{WHITE}')))
        checks += 1
    elif black == 3  ==  checks:
        while True:
            try:
                gulag = int(input(f"{pres}President{END} will place in gulag number (not index): {BOLD}")) - 1; print(END, end='')
                if gulag >= c or gulag < 0 or gulag == pn:
                    raise Exception
            except BaseException as r:
                #print(r)
                print(f"{RED}Wrong syntaxis or too big/small nums{END}")
            else:
                if not input(f"ENTER if number {BOLD}{gulag+1}{END} is right (it's {BOLD}[{g[gulag]}]{END}), else write something: "):
                    break
        logs.append(((g[pn], DEBUG + GULAG + g[gulag] + BLACK_FONT + WHITE), (DEBUG + 'GUL' + WHITE, DEBUG + 'AG' + WHITE, DEBUG + '!' + WHITE, '   ')))
        g[gulag] = GULAG + DEBUG + g[gulag] + WHITE + BLACK_FONT
        checks += 1
        if gulag == hitler:
            degov()
            Git_caput = True
            break
        else:
            Git_not.add(gulag)
    elif black == 4  ==  checks:
        temp = pn
        pn = new_gov("President", pres) - 1
        logs.append(((g[temp], g[pn]), (DEBUG + 'PLA' + WHITE, DEBUG + 'CE' + WHITE, DEBUG + 'D' + WHITE, '   ')))
        checks += 1
        vnf = True
    elif black == 5   == checks:
        while True:
            try:
                killed = int(input(f"{pres}President{END} will kill number (not index): {BOLD}")) - 1; print(END, end='')
                if killed >= c or killed < 0 or killed == pn:
                    raise Exception
            except BaseException as r:
                #print(r)
                print(f"{RED}Wrong syntaxis or too big/small nums{END}")
            else:
                if not input(f"ENTER if number {BOLD}{killed+1}{END} is right (it's {BOLD}[{g[killed]}]{END}), else write something: "):
                    break
        if gulag == killed:
            g[gulag] = g[gulag][10:-10]
            gulag = c
        g[killed] = DEAD + DEBUG + g[killed] + WHITE + BLACK_FONT
        logs.append(((g[pn], g[killed]), (DEBUG + 'KIL' + WHITE, DEBUG + 'LE' + WHITE, DEBUG + 'D' + WHITE, '   ')))
        checks += 1
        if killed not in Git_not:
            if killed == hitler:
                degov()
                Git_caput = True
                break
            else:
                Git_not.add(killed)
    #if red >= 3 and molotov_rebbentrop:
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
        print(f"{RED}{BOLD_2}{UNDERLINE}RED    WON!!!{END}")
        print(f"{RED}{BOLD_2}{UNDERLINE}RED    WON!!!{END}", file=f)
        if Git_caput:
            print(f"{RED}(Hitler caput){WHITE}", file=f)
    elif black >= 6 or Git_cn:
        print(f"{BLACK}{BOLD_2}{UNDERLINE}BLACK    WON!!!{END}")
        print(f"{BLACK}{BOLD_2}{UNDERLINE}BLACK    WON!!!{END}", file=f)
        if Git_cn:
            print(f"{BLACK}(Hitler is cancler){WHITE}", file=f)
    else:
        print(F"{DEBUG}{BOLD_2}{UNDERLINE}WHAT    THE    HELL?!!!!{END}")
        print(F"{DEBUG}{BOLD_2}{UNDERLINE}WHAT    THE    HELL?!!!!{END}", file=f)
    print('\n\n\n', file=f)
    out()
