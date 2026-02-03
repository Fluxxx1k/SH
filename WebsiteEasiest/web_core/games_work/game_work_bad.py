from __future__ import annotations

import os, json, traceback
import random as rnd
import time as t

from WebsiteEasiest.logger import logger
from WebsiteEasiest.web_core.games_players_classes.webplayer import WebPlayer
from core.logs.HTML_logs import color_of_HTML_roles, GameLog, pr_c, purple_c, InfoLog
from legacy import globs
from core.standard_names_SH import X
from user_settings import *
from WebsiteEasiest.data.data_paths import path_logs_games

def game_work_bad(game_name: str, count: int, bots_count: int, first_president: int = 0):
    INFO_LOGS = globs.INFO_LOGS
    ROLES = globs.ROLES
    PLAYERS = globs.PLAYERS
    logger.low_debug(f"{'\n'.join([f'{i}) {j}' for i, j in globs.__dict__.items()])}")
    logger.low_debug(globs.PLAYERS)
    def save_json_of_logs():
        with open(f"{path_logs_games}\\{game_name}.json", 'w+', encoding='utf-8') as file:
            json.dump([log.to_json() for log in normal_logs], file, indent=4)

    code_start_time = t.time()
    INFO_LOGS.append(InfoLog(info_type=X.INFO, info_name="Code start time", info1=t.strftime(f"{DATE_FORMAT} {TIME_FORMAT}"), info2=code_start_time))
    saved = []
    path = f"{DIRECTORY_FOR_GAME_LOGS}\\"
    date = t.strftime(DATE_FORMAT) + ' '
    special_election = False
    skips = 0
    Git_not = set()
    normal_logs: list[GameLog] = globs.GAME_LOGS

    if count == 6:
        red_start = 5
        black_start = 11
    else:
        red_start = 6
        black_start = 11
    deck = ['R'] * red_start + ['B'] * black_start
    try:
        os.makedirs(path, exist_ok=True)
        check_logs = os.listdir(path)
    except Exception as error:
        logger.error(f"{game_name}: Strange Error: {repr(error)}"
                     "\n\tLogs won't be created")
        full_path = None
    else:
        try:
            logs_nums = []
            for i in check_logs:
                if i.startswith(NAME_FOR_GAME_LOGS + game_name + date):
                    logs_nums.append(i)
            max_log_num = len(logs_nums) + 1
            full_path = path + NAME_FOR_GAME_LOGS + game_name + date + str(max_log_num) + EXTENSION_FOR_GAME_LOGS
            while os.path.exists(full_path):
                max_log_num += 1
                logger.warning(f"{game_name}: {full_path}    is already exists, trying {max_log_num}")
                full_path = path + NAME_FOR_GAME_LOGS + game_name + date + str(max_log_num) + EXTENSION_FOR_GAME_LOGS
            open(full_path, 'w+').close()
            logger.info(f"{game_name}: Logs in: {full_path}")
        except Exception as error:
            logger.error(f"{game_name}: Something went wrong, no logs available: {repr(error)}")
            full_path = None
    del logs_nums

    gulag  = None
    killed = None
    HITLER = None
    STALIN = None
    try:
        STALIN = ROLES.index(X.STALIN)
    except ValueError:
        logger.debug(f"{game_name}: No {X.STALIN} in ROLES")
    except Exception as error:
        logger.warning(f"{game_name}: Can't find {X.STALIN= }: {repr(error)}")
    try:
        HITLER = ROLES.index(X.HITLER)
    except ValueError:
        logger.warning(f"{game_name}: WTH? No {X.HITLER} in ROLES...")
    except Exception as error:
        logger.error(f"{game_name}: Can't find {X.HITLER= }: {repr(error)}")

    globs.HITLER = HITLER
    globs.STALIN = STALIN
    globs.COUNT_PLAYERS = count
    start_time = t.time()
    start_time_f = t.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")
    logger.debug(f"{game_name}: Game start time: {start_time_f}")
    INFO_LOGS.append(InfoLog(info_type=X.INFO, info_name="Game start time", info1=start_time_f, info2=start_time))
    red = black = 0
    checks = 1
    Git_caput = False
    Git_cn = False


    def degov() -> None:
        for player_num in range(count):
            PLAYERS[player_num].degov()


    def take_random(c:int) ->  list[str]:
        nonlocal saved
        if saved:
            x = saved.copy()
            saved = []
            return x
        nonlocal deck
        try:
            chosen = rnd.sample(deck, k=c)
        except ValueError:
            normal_logs.append(
                GameLog(special=f"Deck resetting<br>RED: {red_start - red}<br>BLACK: {black_start - black}", is_cards=False))
            save_json_of_logs()
            deck = ["R"] * (red_start - red) + ["B"] * (black_start - black)
            chosen = rnd.sample(deck, k=c)
        for card in chosen:
            deck.remove(card)
        return sorted(chosen)
    pn = first_president
    globs.BOTS = bots_places = get_bot_places(bots_count)
    previous_president:int|None = None
    pn -= 1
    pnc = pn
    cn = None
    while red < RED_WIN_NUM and black < BLACK_WIN_NUM and not Git_caput and not Git_cn:
        if pnc != pn:
            if not special_election:
                pn = (pnc + 1) % count
                pn = (pn + 1) % count
                if pn == gulag:
                    pn = (pn + 1) % count
                if pn == killed:
                    pn = (pn + 1) % count
                if pn == gulag:
                    pn = (pn + 1) % count
        else:
            pn = (pn + 1) % count
            if pn == gulag:
                pn = (pn + 1) % count
            if pn == killed:
                pn = (pn + 1) % count
            if pn == gulag:
                pn = (pn + 1) % count
        if skips % ANARCHY_SKIP_NUM == 0:
                if saved:
                    normal_logs.append(GameLog(special="Cards was shuffled!"))
                    ccp = rnd.sample(saved, k=1)[0]
                else:
                    ccp = take_random(1)[0]
                normal_logs.append(GameLog(prs="ANARCHY", cnc="ANARCHY",
                                           c_cnc_placed=ccp, special=f"({skips} skips)",
                                           is_chancellor=False, is_president=False))
                save_json_of_logs()
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
                    logger.error(f"{game_name}: WTH?!!!! {ccp} isn't 'B' or 'R'")
                saved = 0
                if gulag is not None:
                    normal_logs.append(GameLog(prs="ANARCHY", cnc="ANARCHY", special=f"Anarchy, {PLAYERS[gulag]} freed", is_chancellor=False, is_president=False))
                    save_json_of_logs()
                    PLAYERS[gulag].free()
                    gulag = None
        PLAYERS[pn].chosen_gov(X.PRESIDENT)
        if special_election:
            special_election = False
        else:
            pnc = pn
        cn = PLAYERS[pn].choose_chancellor(cannot_be={previous_president if (count & 1) == 0 else None,
                                                      pn, cn, gulag, killed})
        # print(f"{CYAN}President{END} [{PURPLE}{BOLD}{PLAYERS[pn]}{END}] requested [{PURPLE}{BOLD}{PLAYERS[cn]}{END}] as {YELLOW}chancellor{END}")

        acceptable = 0
        for player in PLAYERS:
            vote = player.vote_for_pair(PLAYERS[pn], PLAYERS[cn])
            INFO_LOGS.append(InfoLog(X.DBG, "Vote info" ,f"{player} voted {vote} for {PLAYERS[pn]} with {PLAYERS[cn]}",
                             info2=t.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            acceptable += vote
        if acceptable > 0:
            INFO_LOGS.append(InfoLog(X.DBG, "Vote info", f"{PLAYERS[pn]} with {PLAYERS[cn]} accepted",
                                     info2=t.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            skips = 0
        else:
            INFO_LOGS.append(InfoLog(X.DBG, "Vote info", f"{PLAYERS[pn]} with {PLAYERS[cn]} disaccepted",
                                     info2=t.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            skips += 1
            degov()
            continue

        if black >= 3 and cn not in Git_not:
            if cn == HITLER:
                degov()
                normal_logs.append(GameLog(prs=PLAYERS[pn], cnc=PLAYERS[cn], special="Hitler is chancellor!"))
                save_json_of_logs()
                Git_cn = True
                break
            else:
                Git_not.add(cn)

        PLAYERS[cn].chosen_gov(X.CHANCELLOR)
        cards = take_random(3)
        c_prs_got = ''.join(cards)
        cps, cards, is_veto = PLAYERS[pn].president(cards, PLAYERS[cn])
        c_cnc_got = ''.join(cards)

        ccs, ccp = PLAYERS[cn].chancellor(cards, pn, cps, is_veto)
        cpsa = PLAYERS[pn].president_said_after_chancellor(cnc=PLAYERS[cn], cards=c_prs_got, ccg=c_cnc_got, ccp=ccp,
                                                           cps=cps, ccs=ccs, )
        if not cpsa:
            cpsa = cps

        if ccp != 'V':
            normal_logs.append(GameLog(prs=PLAYERS[pn], cnc=PLAYERS[cn],
                                       c_prs_got=c_prs_got, c_prs_said=cps, c_prs_said_after=cpsa,
                                       c_cnc_got=c_cnc_got, c_cnc_said=ccs, c_cnc_placed=ccp))
        else:
            normal_logs.append(GameLog(prs=PLAYERS[pn], cnc=PLAYERS[cn],
                                       c_prs_got=c_prs_got, c_prs_said=cps, c_prs_said_after=cpsa,
                                       c_cnc_got=c_cnc_got, c_cnc_said=ccs, c_cnc_placed="",
                                       special="VETO"))
        save_json_of_logs()
        degov()
        previous_president = pn
        if black == 1 >= checks:
            saved = take_random(3)
            cpsc = PLAYERS[pn].check_cards(''.join(saved))
            normal_logs.append(GameLog(prs=PLAYERS[pn],
                                       c_prs_got=''.join(saved),
                                       c_prs_said=cpsc,
                                       special="Card check"))
            save_json_of_logs()
            checks = 2
        elif black == 2 >= checks:
            pc, cpc = PLAYERS[pn].check_player()
            if cpc != PLAYERS[pc].color:
                PLAYERS[pc].black.add(pn)
            normal_logs.append(
                GameLog(prs=PLAYERS[pn], cnc=PLAYERS[pc],
                        special=f"[<font color='{pr_c}'>{PLAYERS[pn]}</font>] said, that color of [<font color='{purple_c}'>{PLAYERS[pc]}</font>] is <font color='{color_of_HTML_roles(cpc)}'>{cpc}</font>",
                        is_chancellor=False))
            save_json_of_logs()
            checks = 3
        elif black == 3 >= checks:
            gulag = PLAYERS[pn].purge_another(X.GULAG)
            normal_logs.append(GameLog(PLAYERS[pn], PLAYERS[gulag], special="In gulag", is_cards=False, is_chancellor=False))
            save_json_of_logs()
            PLAYERS[gulag].purge(X.GULAG)
            if gulag == HITLER:
                degov()
                Git_caput = True
                break
            else:
                Git_not.add(gulag)
            globs.GULAG = gulag
            checks = 4
        elif black == 4 >= checks:
            temp = pn
            pn = PLAYERS[pn].place_another(cannot_be={previous_president if (count & 1) == 0 else None, pn, gulag, killed})
            normal_logs.append(GameLog(PLAYERS[temp], PLAYERS[pn], special="Special placing", is_chancellor=False))
            special_election = True
            checks = 5
        elif black == 5 >= checks:
            killed = PLAYERS[pn].purge_another(X.SHOUT)
            if gulag == killed:
                gulag = None
            PLAYERS[killed].purge(X.KILLED)
            normal_logs.append(GameLog(PLAYERS[pn], PLAYERS[killed], special=f"Killed", is_chancellor=False))
            save_json_of_logs()
            save_json_of_logs()
            if killed not in Git_not:
                if killed == HITLER:
                    degov()
                    Git_caput = True
                    break
                else:
                    Git_not.add(killed)
            globs.KILLED = killed
            checks = 6

    end_time_f = t.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")
    end_time = t.time()
    INFO_LOGS.append(InfoLog(info_type=X.INFO, info_name="Game end time", info1=end_time_f, info2=end_time))
    logger.info(f"{game_name}: Game start time: " + start_time_f)
    logger.info(f"{game_name}: Game over time: " + end_time_f)


def game_process(game_name, count: int, bots_count: int, players: list[str], first_president: int|None = None):
    globs.ROLES = get_roles(count)[0]
    globs.PLAYERS = [WebPlayer(i, players[i], globs.ROLES[i]) for i in range(count)]

    try:
        game_work_bad(game_name, count, bots_count, first_president or 0)
        return True
    except Exception as e:
        logger.critical(f"{game_name}: Error in game_process: {repr(e)}"
                        "\n"f"{traceback.format_exc()}""\n")

        return False
