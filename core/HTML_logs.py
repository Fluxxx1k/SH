import os
import time as t

from core import globs
from core.gamelog import GameLog
from core.infolog import InfoLog
from core.globs import INFO_LOGS, ROLES
from core.standard_functions import color_clear, yes_or_no
from core.standard_names_SH import X
from cli.colors import RESET
from cli.user_color_settings import WARNING, CRITICAL
from core.HTML_colors import *
from Players.abstract_player import AbstractPlayer
from user_settings import IS_PRINT_SMALL_INFO, IS_PRINT_FULL_INFO



def coloring_HTML_cards(s: str, print_errors = IS_PRINT_FULL_INFO, is_print=IS_PRINT_SMALL_INFO) -> str:
    try:
        s = sorted(color_clear(s))
        errs = 0
        s1 = ''
        for i in s:
            if i == "B":
                s1 += f"<font color='{black_c}'>" + i + "</font>"
            elif i == 'R':
                s1 += f"<font color='{red_c}'>" + i + "</font>"
            elif i == 'X':
                s1 += f"<font color='{norm_c}'>" + i + "</font>"
            elif i == 'P':
                s1 += f"<font color='{purple_c}'>" + i + "</font>"
            else:
                if is_print:
                    print(f"{i} should be 'X' or 'R' or 'B' or 'P'")
                errs += 1
                s1 += f"<font color='{norm_c}'>" + i + "</font>"
        return color_clear(s) if errs > 0 else s1
    except Exception as err:
        if print_errors:
            print(f"{WARNING}Error occurred while creating HTML cards: {err}{RESET}")
        elif is_print:
            print(f"{WARNING}Error occurred while creating HTML cards{RESET}")
        return s


def color_of_HTML_roles(s: str, print_errors=IS_PRINT_FULL_INFO, is_print = IS_PRINT_SMALL_INFO) -> str:
    try:
        s = color_clear(s)
        if s in {X.RED, X.STALIN, X.MOLOTOV}:
            return red_c
        if s in {X.BLACK, X.HITLER, X.RIB}:
            return black_c
        if s in {X.ANARCHIST}:
            return nrh_c
        if s.upper() in {'', "NO ROLE"}:
            if is_print:
                print("No role")
            return norm_c
        if print_errors:
            print(f"UNKNOWN ROLE: {s}")
        return norm_c
    except Exception as err:
        if print_errors:
            print(f"{WARNING}Error occurred while creating HTML cards: {err}{RESET}")
        return norm_c


def create_HTML_roles(players: list[AbstractPlayer] = None, roles: list[str] = None, print_errors = IS_PRINT_FULL_INFO, is_print = IS_PRINT_SMALL_INFO) -> str:
    try:
        table_caption = ('\t<caption><h1><b>'
                         'Таблица ролей'
                         '<br>'
                         'Table of roles'
                         '</b></h1></caption>\n')
        table_head = (f"\t<thead>\n"
                        f"\t\t<tr>\n"
                        f"\t\t\t<th style='color: {num_c}'>Number</th>\n"
                        f"\t\t\t<th>Player</th>\n"
                        f"\t\t\t<th>Role</th>"
                        f"\t\t</tr>\n"
                        f"\t</thead>\n")
        if players is None:
            if is_print:
                print("No players specified")
            if roles is None:
                if is_print:
                    print("No roles specified")
                if print_errors:
                    print(f"{WARNING}No players or roles specified")
                    return table_caption + table_head
            else:
                players = ['No name'] * len(roles)
        try:
            if roles is None:
                rls = ['No role'] * len(players)
                if is_print:
                    print(f"{WARNING}No roles specified{RESET}")
            else:
                rls = roles.copy()
        except Exception as err:
            if print_errors:
                print(f"{WARNING}Too old version or smth else: {err}{RESET}")
            if is_print:
                print(f"{WARNING}No roles{RESET}")
            rls = [''] * len(players)
        rows = []
        try:
            for i in range(len(players)):
                try:
                    color = color_of_HTML_roles(color_clear(rls[i]))
                    number = f"\t\t\t<td style=\"color: {num_c}\"><b>{i + 1}</b></td>\n"
                    player = f'\t\t\t<td style="color: {color}"><b>{players[i]}</b></td>\n'
                    role = f'\t\t\t<td style="color: {color}"><b>{rls[i]}</b></td>\n'
                    row = "\t\t<tr>\n" + number + player + role + "\t\t</tr>\n"
                    rows.append(row)
                except Exception as err:
                    if print_errors:
                        print(f"{WARNING}Error occurred while creating HTML roles in cycle: {err}{RESET}")
                        print(rls)
                        print(players)
                    rows.append(f'\t\t<tr>'
                                f'\t\t\t<td style="color: red">{i + 1}</td>\n'
                                f'\t\t\t<td style="color: red">ERROR in row</td>\n'
                                f'\t\t\t<td style="color: red">{err}</td>\n'
                                f' \t\t</tr>\n')
            table_body = f"\t<tbody>\n{''.join(rows)}</tbody>\n"
        except Exception as err:
            try:
                table_body = (f"\t<tbody>\n"
                              f"{''.join(rows)}"
                              f'\t\t<td style="color: red">ERROR</td>\n'
                              f'\t\t<td style="color: red">{err}</td>\n'
                              f'\t\t<td style="color: red"></td>\n'
                              f"</tbody>\n")
            except Exception as err1:
                table_body = ('\t<tbody>\n'
                              f'\t\t<td style="color: red">ERRORS</td>\n'
                              f'\t\t<td style="color: red">{err= }</td>\n'
                              f'\t\t<td style="color: red">{err1= }</td>\n'
                              '\t</tbody>')
            if print_errors:
                print(f"{WARNING}No roles, old version or using cards: {err}{RESET}")
            elif is_print:
                print(f"{WARNING}Error occurred while creating HTML roles{RESET}")
        table = "<table>\n" + table_caption + table_head + table_body + "</table>"
        return table
    except Exception as err:
        if print_errors:
            print(f"{WARNING}Error occurred while creating HTML roles: {err}{WARNING}")
        elif is_print:
            print(f"{WARNING}Error occurred while creating HTML roles{RESET}")
        return ''


def create_HTML_info(print_errors: bool = IS_PRINT_FULL_INFO) -> str:
    table_caption = ("\t<caption><h1><strong>"
                     "Таблица с информацией об игре"
                     "<br>"
                     "Table with information about game"
                     "</strong></h1></caption>\n")
    table_head = (f"\t<thead>\n"
                  f"\t\t<tr>\n"
                  f"\t\t\t<th style=\"color: {num_c}\">Number</th>\n"
                  f"\t\t\t<th style=\"color: {num_c}\">DBG TYPE</th>\n"
                  f"\t\t\t<th>Type of information</th>\n"
                  f"\t\t\t<th>Information-1</th>\n"
                  f"\t\t\t<th>Information-2 (reserve)</th>\n"
                  f"\t\t</tr>\n"
                  f"\t</thead>\n")
    table_body = ''
    try:
        rows = []
        logs = INFO_LOGS[:99]
        if len(INFO_LOGS) > 99:
            print(f"{CRITICAL}ATTENTION! \n{WARNING}Too many errors, len of info_name is {len(INFO_LOGS)} (You still can play? may be){RESET}")
        for log_i in range(len(logs)):
            try:
                row = logs[log_i].to_HTML_row(log_i + 1)
                rows.append(row)
            except Exception as err:
                INFO_LOGS.append(
                    InfoLog(info_type=X.WARNING, info_name="Error occurred while creating HTML logs info_name",
                            info1=f"{repr(err)}"))
                if print_errors:
                    print(f"{WARNING}Error occurred while creating HTML info_name: {err}{RESET}")
                else:
                    print(f"{WARNING}Error occurred while creating HTML info_name{RESET}")

        rows.append(InfoLog(X.INFO, 'Log creating moment', t.strftime("%d.%m.%y %H:%M:%S"), t.time()).to_HTML_row(min(len(rows) + 1, 100)))
        table_body = "\t<tbody>\n" + ''.join(rows) + "\n\t</tbody>"
    except Exception as err:
        INFO_LOGS.append(
            InfoLog(info_type=X.ERROR, info_name="Error occurred while creating HTML logs", info1=f"{repr(err)}"))
        if print_errors:
            print(f"{WARNING}Error occurred while creating HTML info_name: {err}{RESET}")
    table = "<table>\n" + table_caption + table_head + table_body + "\n</table>"
    return table


def create_HTML_logs_cards(logs, print_errors = IS_PRINT_FULL_INFO, is_print = IS_PRINT_SMALL_INFO) -> str:
    try:
        table_caption = ("<caption><h1><strong>"
                         "Таблица событий игры"
                         "<br>"
                         "Logs of the game"
                         "</strong></h1></caption>\n")
        table_head = (f"<thead>"
                        f"\t<tr>"
                        f"\t\t<th style=\"color: {num_c}\">N</th>"
                        f"\t\t<th style=\"color: {pr_c}\">President</th>"
                        f"\t\t<th style=\"color: {ch_c}\">Chancellor</th>"
                        f"\t\t<th>Cards <font color=\"{pr_c}\">President</font> Got</th>"
                        f"\t\t<th>Cards <font color=\"{pr_c}\">President</font> Said</th>"
                        f"\t\t<th>Cards <font color=\"{ch_c}\">Chancellor</font> Got</th>"
                        f"\t\t<th>Cards <font color=\"{ch_c}\">Chancellor</font> Said</th>"
                        f"\t\t<th>Card <font color=\"{ch_c}\">Chancellor</font> Placed</th>"
                        f"\t\t<th>Cards <font color=\"{pr_c}\">President</font> Said After <font color=\"{ch_c}\">Chancellor</font></th>"
                        f"\t\t<th><font color=\"{special_c}\">Special</font></th>"
                        f"\t</tr>"
                        f"</thead>")

        table_body = "<tbody>"
        rows = []
        for i in range(len(logs)):
            log = logs[i]
            number = f'\t\t<td style="color: {num_c}">{i + 1}</td>\n'
            cooked = log.to_HTML_row()
            row = "\t<tr>" + number + cooked + '</tr>'
            rows.append(row)
        table_body += '\n'.join(rows)
        table_body += '\n</tbody>'
        table = "<table>\n" + table_caption + '\n' + table_head + '\n' + table_body + '\n</table>'
        return table
    except Exception as err:
        if print_errors:
            print(f"{CRITICAL}Error occurred while creating HTML logs about cards: {err}{RESET}")
        elif is_print:
            print(f"{CRITICAL}Error occurred while creating HTML logs about cards{RESET}")
        INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name="Error occurred while creating HTML logs about cards",
                                 info1=f"{repr(err)}"))
        return ''

def create_HTML_logs_cards_for_Website(logs=None, print_errors = IS_PRINT_FULL_INFO, is_print = IS_PRINT_SMALL_INFO) -> str:
    head = """
                 <style>
                     .table1 {
                         border:5px solid """ + norm_c + """;
                         bgcolor: #222;
                         padding: 10px;
                         cellpadding: 10px;
                         cellspacing: 2px;
                         border-collapse: collapse;
                         width: 100%;
                         margin-bottom: 20px;
                     }
                     .table1 th {
                         border: 3px """ + norm_c + """ solid;
                     }
                     .table1 td {
                         border: 2px """ + norm_c + """ solid;
                     }
                 </style>
             """
    if logs is None:
        logs = globs.GAME_LOGS
    try:
        # table_caption = ("<caption><h1><strong>"
        #                  "Таблица событий игры"
        #                  "<br>"
        #                  "Logs of the game"
        #                  "</strong></h1></caption>\n")
        table_head = (f"<thead>"
                        f"\t<tr>"
                        f"\t\t<th style=\"color: {num_c}\">N</th>"
                        f"\t\t<th style=\"color: {pr_c}\">President</th>"
                        f"\t\t<th style=\"color: {ch_c}\">Chancellor</th>"
                        # f"\t\t<th>Cards <font color=\"{pr_c}\">President</font> Got</th>"
                        f"\t\t<th>Cards <font color=\"{pr_c}\">President</font> Said</th>"
                        # f"\t\t<th>Cards <font color=\"{ch_c}\">Chancellor</font> Got</th>"
                        f"\t\t<th>Cards <font color=\"{ch_c}\">Chancellor</font> Said</th>"
                        f"\t\t<th>Card <font color=\"{ch_c}\">Chancellor</font> Placed</th>"
                        f"\t\t<th>Cards <font color=\"{pr_c}\">President</font> Said After <font color=\"{ch_c}\">Chancellor</font></th>"
                        f"\t\t<th><font color=\"{special_c}\">Special</font></th>"
                        f"\t</tr>"
                        f"</thead>")

        table_body = "<tbody>"
        rows = []
        for i in range(len(logs)):
            log = logs[i]
            number = f'\t\t<td style="color: {num_c}">{i + 1}</td>\n'
            cooked = log.to_HTML_row()
            row = "\t<tr>" + number + cooked + '</tr>'
            rows.append(row)
        table_body += '\n'.join(rows)
        table_body += '\n</tbody>'
        table = head+ f"<table class=\"table1\">\n" + table_head + '\n' + table_body + '\n</table>'
        return table
    except Exception as err:
        if print_errors:
            print(f"{CRITICAL}Error occurred while creating HTML logs about cards: {err}{RESET}")
        elif is_print:
            print(f"{CRITICAL}Error occurred while creating HTML logs about cards{RESET}")
        INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name="Error occurred while creating HTML logs about cards",
                                 info1=f"{repr(err)}"))
        return ''

def create_HTML_logs(path: str, logs: list[GameLog], players: list[AbstractPlayer] = None, *args, **kwargs) -> str:
    try:
        if args:
            if IS_PRINT_FULL_INFO:
                print(f"{WARNING}Too many arguments provided: {args}{RESET}")
            elif IS_PRINT_SMALL_INFO:
                print(f"{WARNING}too many arguments{RESET}")
            INFO_LOGS.append(
                InfoLog(info_type=X.WARNING, info_name=f"Too many arguments provided", info1=' '.join(args)))
        if kwargs:
            if IS_PRINT_FULL_INFO:
                print(f"{WARNING}Too many keyword arguments provided: {kwargs}{RESET}")
            elif IS_PRINT_SMALL_INFO:
                print(f"{WARNING}Too many keyword arguments{RESET}")
            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Too many keyword arguments provided",
                                     info1=' '.join([f"({i}: {j})" for i, j in kwargs.items()])))
        if not os.path.exists(path):
            print(f"{CRITICAL}Path is wrong!{RESET}")
            if yes_or_no(f"Create path ({path}) to file? "):
                try:
                    os.makedirs(path)
                except PermissionError as err:
                    print(f"{CRITICAL}Error occurred while creating path: {type(err)}({err}){RESET}")
                    INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name="Error occurred while creating all HTML logs",
                                             info1=f"{repr(err)}"))
                except Exception as err:
                    INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name="Error occurred while creating HTML logs",
                                             info1=f"{repr(err)}"))
                    print(f"{CRITICAL}Error occurred while creating path: {type(err)}({err}){RESET}")
                    return ''
            else:
                print("OK, No logs")
                return ''
    except Exception as err:
        if IS_PRINT_FULL_INFO:
            print(f"{CRITICAL}Unexpected error occurred while creating HTML logs: {err}{RESET}")
        else:
            print(f"{CRITICAL}Unexpected error occurred while creating HTML logs{RESET}")
    try:
        head = """
         <head>
             <meta charset='UTF-8'>
             <title>Secret Hitler logs</title>
             <style>
                 body {
                     color:""" + norm_c + """;
                     background-color: """ + font_c + """;
                 }
                 table {
                     border:5px solid """ + norm_c + """;
                     bgcolor: #222;
                     padding: 10px;
                     cellpadding: 10px;
                     cellspacing: 2px;
                     border-collapse: collapse;
                     width: 100%;
                     margin-bottom: 20px;
                 }
                 th {
                     border: 3px """ + norm_c + """ solid;
                 }
                 td {
                     border: 2px """ + norm_c + """ solid;
                 }
             </style>
         </head>
         """

        try:
            table_roles = create_HTML_roles(players, ROLES)
        except Exception as err:
            table_roles = ''
            print(f"Oops, something went wrong: {err}")
            print(f"{WARNING}Table of roles could not be created{RESET}")
        try:
            table_info = create_HTML_info()
        except Exception as err:
            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name="Error occurred while creating HTML info_name logs",
                                     info1=f"{repr(err)}"))
            table_info = ''
            print(f"Oops, something went wrong: {err}")
            print(f"{WARNING}Table with information could not be created{RESET}")
        try:
            table_logs = create_HTML_logs_cards(logs)
        except Exception as err:
            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name="Error occurred while creating HTML cards logs",
                                     info1=f"{repr(err)}"))
            table_logs = ''
            print(f"Oops, something went wrong: {err}")
            print(f"{CRITICAL}Table of logs with cards could not be created{RESET}")

        body = ("<body>\n" +
                table_roles +
                '\n' +
                table_logs +
                '\n' +
                table_info +
                '\n</body>')
        s = ("<!DOCTYPE html>\n"
             "<html>\n" +
             head +
             '\n' +
             body +
             '\n</html>\n')
        with open(path, 'w+', encoding="UTF-8") as f:
            print(s, file=f)
        return s
    except Exception as err:
        INFO_LOGS.append(
            InfoLog(info_type=X.ERROR, info_name="Error occurred while creating all HTML logs", info1=f"{repr(err)}"))
        print(f"Oops, something went wrong: {err}")
        print(f"{CRITICAL}HTML Table of logs could not be created!!!{RESET}")
        return ''

