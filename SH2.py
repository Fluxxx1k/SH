import os
import random as rnd
import sys
import time as t
from atexit import register as atexit

from HTML_logs import create_HTML_logs, color_of_HTML_roles, Log, pr_c, purple_c
from colors import (YELLOW_TEXT_BRIGHT as YELLOW,
                    BLUE_TEXT_BRIGHT as BLUE,
                    CYAN_TEXT_BRIGHT as CYAN,
                    PURPLE_TEXT_BRIGHT as PURPLE,
                    RED_TEXT_BRIGHT as RED,
                    GREEN_TEXT_BRIGHT as BLACK,
                    RESET_TEXT as END_T,
                    RESET_BACKGROUND as END_BG,
                    YELLOW_BACKGROUND as GULAG,
                    END, BOLD, UNDERLINE,
                    )
from player import Player  # , Bot
from globs import PLAYERS, ROLES
from standard_functions import show_only_to_one, yes_or_no
from standard_names_SH import X
from user_color_settings import INPUT_COLOR, CRITICAL, WARNING, GOOD
from user_settings import *
from utils import coloring, naming, get_color, input_cards

ff = __file__
print(ff)
saved = []
path = os.path.dirname(ff) + "/LOGS/"
date = t.strftime("%d.%m.%y ")
MAX_NAME_LEN = 15  # You can change it from 10 to infinity
LEN_FOR_TABLET = MAX_NAME_LEN + max(len(CYAN), len(YELLOW)) + len(END_T)
special_election = False
skips = 0
logs: list[tuple[tuple[str, str], tuple[str, str, str, str]]] = []
Git_not = set()
print(f"If will be error say it to coder (DS: {PURPLE}@fluxxx1k{END})")
normal_logs: list[Log] = []


# Number of players and their names
while True:
    try:
        c = int(input(f"Input number of players: {INPUT_COLOR}"))
        print(END, end='')
        if c < MIN_PLAYER_NUM or c > MAX_PLAYER_NUM:
            raise ValueError(f"Wrong size! ({c})")
    except BaseException as fixes:
        print(f"{RED}Try again, wrong input: {fixes}{END_T}")
    else:
        if not input(f"If you are sure that here will be {c} gamers press ENTER else write anything: "):
            break
if c == 6:
    print(f"{INPUT_COLOR}5 {RED}RED{PURPLE} cards, 11 {BLACK}BLACK{PURPLE} cards{END}")
    red_start = 5
    black_start = 11
else:
    print(f"{INPUT_COLOR}6 {RED}RED{PURPLE} cards, 11 {BLACK}BLACK{PURPLE} cards{END}")
    red_start = 6
    black_start = 11
deck = ['R'] * red_start + ['B'] * black_start
try:
    os.makedirs(path, exist_ok=True)
    check_logs = os.listdir(path)
except BaseException as fixes:
    print(f"{CRITICAL}Strange Error: {fixes}\nLogs won't be created{END}")
    full_path = None
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
    except BaseException as fixes:
        print(f"{CRITICAL}Something went wrong, no logs available: {fixes}{END}")
        full_path = None
gulag = MAX_PLAYER_NUM
killed = MAX_PLAYER_NUM
hitler = MAX_PLAYER_NUM
stalin = MAX_PLAYER_NUM
ROLES, molotov_ribbentrop = get_roles(c)

try:
    stalin = ROLES.index(X.STALIN)
except ValueError:
    print("No Sosalin :_((")
except BaseException as fixes:
    print(f"Can't find {X.STALIN= }: {fixes}")
try:
    hitler = ROLES.index(X.HITLER)
except ValueError:
    print(f"{WARNING}WTH? No {X.HITLER} in ROLES...{END}")
except BaseException as fixes:
    print(f"Can't find {X.HITLER= }: {fixes}")

start_time = t.time()
start_time_f = t.strftime("%d.%m.%y %H:%M:%S")
print(start_time_f)
red = black = 0
checks = 1
Git_caput = False
Git_cn = False
f_l = {"OUT", "DEBUG_MODE", "EXIT"}



def out(count = c, file=sys.stdout):
    for player_num in range(count):
        print(f"№{player_num + 1}) {PLAYERS[player_num].out()}", file=file)



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
    create_HTML_logs(path=full_path, logs=normal_logs, players=PLAYERS, roles=ROLES)
    logged = 1
    try:
        print(
            f"{END}{UNDERLINE}{BOLD}{TABLE_SPLITTER} {CYAN + 'President' + END_T: <{LEN_FOR_TABLET}} {TABLE_SPLITTER} {YELLOW + 'Chancellor' + END_T: <{LEN_FOR_TABLET}} {TABLE_SPLITTER} CPS {TABLE_SPLITTER} CCS {TABLE_SPLITTER} CCP {TABLE_SPLITTER} CPSA {TABLE_SPLITTER}{END}")
        for log in logs:
            logged += 1
            print(
                f"{END}{UNDERLINE}{BOLD}{TABLE_SPLITTER} {CYAN + log[0][0] + END_T: <{LEN_FOR_TABLET}} {TABLE_SPLITTER} {YELLOW + log[0][1] + END_T: <{LEN_FOR_TABLET}} {TABLE_SPLITTER} {log[1][0] + END_T: <8} {TABLE_SPLITTER} {log[1][1] + END_T: <7}  {TABLE_SPLITTER} {log[1][2] + END_T: <6}   {TABLE_SPLITTER} {(log[1][3] if len(log[1]) >= 4 else 'XXX') + END_T: <8}  {TABLE_SPLITTER}{END}")
    except BaseException as err:
        print(err)
        try:
            normal_logs.append(
                Log(prs=f"{logged= }", cnc=f"{len(logs)= }", special=f"{type(err)}({err})", is_president=False, is_chancellor=False))
        except BaseException as err:
            print(err)
        logged -= 1
        print(
            f"{END}{UNDERLINE}{BOLD}{TABLE_SPLITTER} {CYAN + 'President' + END_T: <{LEN_FOR_TABLET}} {TABLE_SPLITTER} {YELLOW + 'Chancellor' + END_T: <{LEN_FOR_TABLET}} {TABLE_SPLITTER} CPS {TABLE_SPLITTER} CCS {TABLE_SPLITTER} CCP {TABLE_SPLITTER} CPSA {TABLE_SPLITTER}{END}")
        for log in logs:
            logged -= 1
            if logged:
                print(
                    f"{END}{UNDERLINE}{BOLD}{TABLE_SPLITTER} {CYAN + log[0][0] + END_T: <{LEN_FOR_TABLET}} {TABLE_SPLITTER} {YELLOW + log[0][1] + END_T: <{LEN_FOR_TABLET}} {TABLE_SPLITTER} {log[1][0] + END_T: <8} {TABLE_SPLITTER} {log[1][1] + END_T: <7}  {TABLE_SPLITTER} {log[1][2] + END_T: <6}   {TABLE_SPLITTER} {(log[1][3] if len(log[1]) >= 4 else 'XXX') + END_T: <8}  {TABLE_SPLITTER}{END}")
            else:
                print(*log, sep=f'{END} {TABLE_SPLITTER} {END}')


def new_gov(gov_type:str=f"GOVERNMENT", color:str=BLUE) -> int:
    while True:
        try:
            gov = int(input(f"{color}{gov_type}{END_T}'s number (not index): {INPUT_COLOR}")) - 1
            print(END, end='')
            if gov >= c or gov < 0:
                raise ValueError(f"Wrong number: {gov + 1}")
            if gov == pn:
                raise ValueError(f"Can't choose president as a {gov_type}")
            if  gov == gulag or gov == killed:
                raise ValueError("Can't choose purged as s chancellor")
        except BaseException as err:
            print(f"{RED}{err}{END}")
        else:
            if not input("ENTER if number is right, else write something: "):
                break
    return gov


def degov() -> None:
    for player_num in range(c):
        PLAYERS[player_num].degov()

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
    elif cmd == '' or cmd == 'EXIT':
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
        print(f"{PURPLE+BOLD}DECK RESET!!!{END}")
        logs.append(((PURPLE + f'{"DECK":<{MAX_NAME_LEN}}' + END_T, PURPLE + f'{"RESET":<{MAX_NAME_LEN}}' + END_T),
                     (f'{BLACK}BLK{END_T}', f'{BLACK}{str(black_start-black):>2}{END_T}', f'{RED}{red_start-red}{END_T}', f'{RED}RED{END_T}')))
        normal_logs.append(
            Log(special=f"Deck resetting<br>RED: {red_start - red}<br>BLACK: {black_start - black}", is_cards=False))
        deck = ["R"] * (red_start - red) + ["B"] * (black_start - black)
        chosen = rnd.sample(deck, k=count)
        logs_out()
    for card in chosen:
        deck.remove(card)
    return chosen



for i in range(c):
    pl_name = input(f"GAYmer №{i + 1}) {INPUT_COLOR}")
    print(END, end='')
    while len(pl_name) > MAX_NAME_LEN or len(pl_name) < MIN_NAME_LEN or pl_name in PLAYERS:
        print(f"{RED}Length of name should be 1-{MAX_NAME_LEN} symbols!{END}")
        pl_name = input(f"{RED}New attempt:{END} GAYmer №{i + 1}) {INPUT_COLOR}")
        print(END, end='')

    PLAYERS.append(Player(num=i, name=pl_name, role=ROLES[i]))
fixes = []
while True:
    try:
        fixes = list(map(int, input(f"Print numbers of mistakes: {INPUT_COLOR}").split()))
        print(END, end='')
        for i in fixes:
            if i > c or i < 1:
                raise ValueError(f"Wrong number: {i}")
    except BaseException as fixes:
        print(f"{RED}{fixes}{END}")
    else:
        break
for i in fixes:
    pl_name = input(f"{PURPLE}Fixing names:{END} GAYmer №{i}) {INPUT_COLOR}").strip()
    print(END, end='')
    while len(pl_name) > MAX_NAME_LEN or pl_name == '' or pl_name in PLAYERS:
        print(f"{RED}Length of name should be 1-{MAX_NAME_LEN} symbols!{END}")
        pl_name = input(f"{RED}New try:{END} GAYmer №{i}) {INPUT_COLOR}").strip()
        print(END, end='')
    PLAYERS[i - 1] = Player(num=i - 1, name=pl_name, role=ROLES[i - 1])
print(*list(map(repr, PLAYERS)), sep='\n')

for i in range(c):
    print(f"{PURPLE}{INPUT_COLOR}[{PLAYERS[i]}]{END}, come here to get your role!")
    show_only_to_one(f"Your role is: {INPUT_COLOR}{naming(ROLES[i])}{END}", 25)

while True:
    try:
        pn = int(input(f"{CYAN}President{END}'s number (not index): {INPUT_COLOR}")) - 1
        print(END, end='')
        if pn >= c or pn < 0:
            raise ValueError(f"Wrong number: {pn + 1}")
    except BaseException as fixes:
        print(f"{RED}{fixes}{END}")
    else:
        if not input("ENTER if number is right, else write something: "):
            break
pn -= 1
pnc = pn
while red < RED_WIN_NUM and black < BLACK_WIN_NUM and not Git_caput and not Git_cn:
    if pnc != pn:
        if special_election:
            print(f"{PURPLE}{pnc = } != {pn = } => Внеоф{END_T}")
        else:
            # print(f"{PURPLE}WTF?!! (Line 160)")
            print(f"{PURPLE}{pnc = } != {pn = } but {special_election = }{END_T}")
            pn = pnc
    if skips >= ANARCHY_SKIP_NUM:
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
                logs.append(((f"{PURPLE + 'ANARCHY' + END_T: <{LEN_FOR_TABLET}}", PLAYERS[gulag].table()),
                             (f'{PURPLE}FRE{END_T}', f'{PURPLE}E!{END_T}', f'{PURPLE}!{END_T}', '   ')))
                print(f"{PURPLE}{PLAYERS[gulag]} was de-Gulag-ed{END_T}")
                normal_logs.append(Log(special=f"Anarchy, {PLAYERS[gulag]} freed"))
                PLAYERS[gulag].free()
                gulag = MAX_PLAYER_NUM
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
    PLAYERS[pn].chosen_gov(X.PRESIDENT)
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
        if MAX_PLAYER_NUM <= stalin:
            if cn == hitler:
                degov()
                logs.append(((PLAYERS[pn].table(), PLAYERS[cn].table()),
                             (f'{BLACK}HIT{END_T}', f'{BLACK}LE{END_T}', f'{BLACK}R{END_T}', '   ')))
                normal_logs.append(Log(prs=PLAYERS[pn], cnc=PLAYERS[cn], special="Hitler is chancellor!"))
                Git_cn = True
                break
            else:
                Git_not.add(cn)
        else:
            if hitler == cn:
                if yes_or_no(f"Is {PLAYERS[cn]} hitler "):
                    degov()
                    logs.append(((PLAYERS[pn].table(), PLAYERS[cn].table()),
                                 (f'{BLACK}HIT{END_T}', f'{BLACK}vs{END_T}', f'{BLACK}S{END_T}', 'TAL')))
                    normal_logs.append(
                        Log(prs=PLAYERS[pn], cnc=PLAYERS[cn], special="Hitler is chancellor!<br>But Stalin is president!"))
                    Git_caput = True
                    break
            else:
                yes_or_no(f"Is {PLAYERS[cn]} hitler? ", yes=set())
    PLAYERS[cn].chosen_gov(X.CHANCELLOR)
    out()
    cards = take_random(3)
    c_prs_got = ''.join(cards)
    cps, cards, is_veto = PLAYERS[pn].president(cards, PLAYERS[cn], black=black, red=red)
    c_cnc_got = ''.join(cards)
    ccs, ccp = PLAYERS[cn].chancellor(cards, pn, cps, is_veto, black=black, red=red)
    # cpsa = input_cards(f"Cards {CYAN}president{END_T} ({players[pn]}) said after chancellor: ", q={3, 0})
    cpsa = PLAYERS[pn].president_said_after_chancellor(cnc=PLAYERS[cn], cards=c_prs_got, ccg=c_cnc_got, ccp=ccp,
                                                       cps=cps, ccs=ccs, )
    temp = input(f'Command: {INPUT_COLOR}').upper()
    print(END, end='')
    while comm(temp):
        temp = input(f'Command (new try): {INPUT_COLOR}').upper()
        print(END, end='')
    if ccp == 'B' or ccp == BLACK + "B" + END_T:
        black += 1
    elif ccp == 'R' or ccp == RED + "R" + END_T:
        red += 1
    elif ccp == 'P' or ccp == PURPLE + "P" + END_T:
        red += 1
        black += 1
    elif (ccp == 'VETO' or ccp == "X") and black >= 5:
        print(f"{GOOD}{PURPLE}VETO{END_T}")
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
        normal_logs.append(Log(prs=PLAYERS[pn], cnc=PLAYERS[cn],
                               c_prs_got=c_prs_got, c_prs_said=cps, c_prs_said_after=cpsa,
                               c_cnc_got=c_cnc_got, c_cnc_said=ccs, c_cnc_placed=ccp))
    else:
        normal_logs.append(Log(prs=PLAYERS[pn], cnc=PLAYERS[cn],
                               c_prs_got=c_prs_got, c_prs_said=cps, c_prs_said_after=cpsa,
                               c_cnc_got=c_cnc_got, c_cnc_said=ccs, c_cnc_placed="",
                               special="VETO"))
        ccp = PURPLE + "V" + END_T
    cpsa = coloring(cpsa)
    degov()
    print("\n\n\n")

    logs.append(((PLAYERS[pn].table(), PLAYERS[cn].table()), (cps, ccs, ccp, cpsa)))
    if black == 1 == checks:
        saved = take_random(3)
        show_only_to_one(coloring(saved))
        cpsc = input_cards(f"Cards {CYAN}president{END} said after checking: ", q=3)
        cpsc = coloring(cpsc)
        logs.append(((PLAYERS[pn].table(), f"{PURPLE + 'CARD CHECK' + END_T: <{LEN_FOR_TABLET}}"),
                     (cpsc, PURPLE + 'CH' + END_T, PURPLE + 'K' + END_T, '   ')))
        normal_logs.append(Log(prs=PLAYERS[pn], c_prs_got=''.join(saved), c_prs_said=cpsc, special="Card check"))
        checks += 1
    elif black == 2 == checks:
        while True:
            try:
                pc = int(input(f"{CYAN}President{END} will check number (not index): {INPUT_COLOR}")) - 1
                print(END, end='')
                if pc >= c or pc < 0:
                    raise ValueError(f"Wrong number: {pc + 1}")
                if pc == pn:
                    raise ValueError(f"Can't check yourself")
            except BaseException as fixes:
                print(f"{RED}{fixes}{END}")
            else:
                if not input(
                        f"ENTER if number {INPUT_COLOR}{pc + 1}{END} is right (it's {INPUT_COLOR}[{PLAYERS[pc]}]{END}), else write something: "):
                    break
        show_only_to_one(f"Color is {get_color(ROLES[pc])}")
        print(f"Input {BLACK}BLK{END} or {RED}RED{END}")
        cpc = input(f"Color of {PLAYERS[pc]} {CYAN}President{END} said: {INPUT_COLOR}").upper()
        print(END, end='')  # card_chancellor_placed
        while cpc not in {X.BLACK, X.RED, X.NRH}:
            print(f"{RED}WRONG    INPUT{END}")
            cpc = input(f"Color of {PURPLE}{PLAYERS[pc]}{END_T} {CYAN}President{END_T} said: {INPUT_COLOR}").upper()
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
            ((PLAYERS[pn].table(), PURPLE + PLAYERS[pc].table() + END_T),
             (cpc1, PURPLE + 'CH' + END_T, PURPLE + 'K' + END_T, f'{PURPLE}PLR{END_T}')))
        normal_logs.append(
            Log(prs=PLAYERS[pn], cnc=PLAYERS[cn],
                special=f"Color of <font color='{purple_c}'>{PLAYERS[cn]}</font> <font color='{pr_c}'>{PLAYERS[pn]}</font> said is <font color='{color_of_HTML_roles(cpc)}'>{cpc}</font>",
                is_chancellor=False))
        checks += 1
    elif black == 3 == checks:
        while True:
            try:
                gulag = int(input(f"{CYAN}President{END} will place in gulag number (not index): {INPUT_COLOR}")) - 1
                print(END, end='')
                if gulag >= MAX_PLAYER_NUM or gulag < 0:
                    raise ValueError(f"Wrong number: {gulag + 1}")
                if gulag == pn:
                    raise ValueError(f"Can't purge yourself")
            except BaseException as fixes:
                print(f"{RED}{fixes}{END}")
            else:
                if not input(
                        f"ENTER if number {INPUT_COLOR}{gulag + 1}{END} is right (it's {INPUT_COLOR}[{PLAYERS[gulag]}]{END}), else write something: "):
                    break
        logs.append(((PLAYERS[pn].table(), PURPLE + GULAG + PLAYERS[gulag].table() + END_BG + END_T),
                     (PURPLE + 'GUL' + END_T, PURPLE + 'AG' + END_T, PURPLE + '!' + END_T, '   ')))
        normal_logs.append(Log(PLAYERS[pn], PLAYERS[gulag], special="In gulag", is_cards=False, is_chancellor=False))
        PLAYERS[gulag].purge(X.GULAG)
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
        logs.append(((PLAYERS[temp].table(), PLAYERS[pn + 1].table()),
                     (PURPLE + 'PLA' + END_T, PURPLE + 'CE' + END_T, PURPLE + 'D' + END_T, '   ')))
        normal_logs.append(Log(PLAYERS[temp], PLAYERS[pn + 1], special="Special placing", is_chancellor=False))
        checks += 1
        special_election = True
    elif black == 5 == checks:
        while True:
            try:
                killed = int(input(f"{CYAN}President{END} will kill number (not index): {INPUT_COLOR}")) - 1
                print(END, end='')
                if killed >= MAX_PLAYER_NUM or killed < 0:
                    raise ValueError(f"Wrong number: {killed + 1}")
                elif killed == pn:
                    raise ValueError("No suicide!!")
            except BaseException as fixes:
                print(f"{RED}{fixes}{END}")
            else:
                if not input(
                        f"ENTER if number {INPUT_COLOR}{killed + 1}{END} is right (it's {INPUT_COLOR}[{PLAYERS[killed]}]{END}), else write something: "):
                    break
        if gulag == killed:
            gulag = MAX_PLAYER_NUM
        PLAYERS[killed].purge(X.KILLED)
        logs.append(((PLAYERS[pn].table(), PLAYERS[killed].table()),
                     (PURPLE + 'KIL' + END_T, PURPLE + 'LE' + END_T, PURPLE + 'D' + END_T, '   ')))
        normal_logs.append(Log(PLAYERS[pn], PLAYERS[killed], special=f"Killed", is_chancellor=False))
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
            print(f'№{i + 1}) {PLAYERS[i]}')
        print('\n')

logs_out()
try:
    # raise MyErr("Not available now")
    with open(full_path, "a+", encoding="UTF-8") as f:
        end_time_f = t.strftime("%d.%m.%y %H:%M:%S")
        end_time = t.time()
        print("Game start time: " + start_time_f)
        print("Game over time: " + end_time_f)
        # print("Game start time: " + start_time_f, file=f)
        # print("Game over time: " + end_time_f, file=f)

        if red >= RED_WIN_NUM or Git_caput:
            print(f"{RED}{BOLD}{UNDERLINE}RED    WON!!!{END}")
            # print(f"{RED}{BOLD}{UNDERLINE}RED    WON!!!{END}", file=f)
            if Git_caput:
                print(f"{RED}(Hitler caput){END_T}")
                # print(f"{RED}(Hitler caput){END_T}", file=f)
        elif black >= BLACK_WIN_NUM or Git_cn:
            print(f"{BLACK}{BOLD}{UNDERLINE}BLACK    WON!!!{END}")
            # print(f"{BLACK}{BOLD}{UNDERLINE}BLACK    WON!!!{END}", file=f)
            if Git_cn:
                print(f"{BLACK}(Hitler is chancellor){END_T}")
                # print(f"{BLACK}(Hitler is chancellor){END_T}", file=f)
        else:
            print(F"{PURPLE}{BOLD}{UNDERLINE}WHAT    THE    HELL?!!!!{END}")
            # print(F"{PURPLE}{BOLD}{UNDERLINE}WHAT    THE    HELL?!!!!{END}", file=f)
        # print('\n\n\n', file=f)
        # out()
except FileNotFoundError:
    print("Can't open file")
except BaseException as fixes:
    print(f"{RED}{BOLD}{UNDERLINE}Something went wrong: {fixes}{END}")