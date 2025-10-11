from standard_functions import color_clear
from standard_names_SH import *
from colors import CRITICAL, WARNING, RESET
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


def coloring_HTML_cards(s: str, print_errors = True) -> str:
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
                s1 += f"<font color='{norm_c_cut}'>" + i + "</font>"
            elif i == 'P':
                s1 += f"<font color='{purple_c}'>" + i + "</font>"
            else:
                print(f"{i} should be 'X' or 'R' or 'B' or 'P'")
                errs += 1
                s1 += f"<font color='{norm_c_cut}'>" + i + "</font>"
        return color_clear(s) if errs > 0 else s1
    except BaseException as err:
        if print_errors:
            print(f"{WARNING}Error occurred while creating HTML cards: {err}{RESET}")
        return s


def color_of_HTML_roles(s: str, print_errors=True) -> str:
    try:
        s = color_clear(s)
        if s in {X.RED, X.STALIN, X.MOLOTOV}:
            return red_c
        if s in {X.BLACK, X.HITLER, X.RIB}:
            return black_c
        if s in {X.ANARCHIST}:
            return nrh_c
        if s in '':
            if print_errors:
                print("No role")
            return norm_c
        if print_errors:
            print(f"UNKNOWN ROLE: {s}")
        return norm_c
    except BaseException as err:
        if print_errors:
            print(f"{WARNING}Error occurred while creating HTML cards: {err}{RESET}")
        return norm_c


def create_HTML_roles(players: list["Player"] = None, roles: list[str] = None, print_errors = True, is_print = True) -> str:
    try:
        if players is None:
            if is_print:
                print("No players specified")
            return ''
        s = '<table>\n<caption><h1><b>Таблица ролей<br>Table of roles</b></h1></caption>'
        table_header = f"<tr><th>Number</th><th>Player</th><th>Role</th></tr>\n"
        s += table_header
        rows = []
        try:
            if roles is None:
                rls = [''] * len(players)
                if is_print:
                    print(f"{WARNING}No roles specified{RESET}")
            else:
                rls = roles.copy()
        except BaseException as err:
            if print_errors:
                print(f"{WARNING}Too old version or smth else: {err}{RESET}")
            if is_print:
                print(f"{WARNING}No roles{RESET}")
            rls = [''] * len(players)
        try:
            for i in range(len(players)):
                color = color_of_HTML_roles(color_clear(rls[i]))
                number = f"<td style=\"color: {num_c}\"><b>{i + 1}</b></td>"
                player = f'<td style="color: {color}"><b>{players[i]}</b></td>'
                role = f'<td style="color: {color}"><b>{rls[i]}</b></td>'
                row = "<tr>" + number + player + role + "</tr>"
                rows.append(row)
            s += '\n'.join(rows)
        except BaseException as err:
            if print_errors:
                print(f"{WARNING}No roles, old version or using cards: {err}{RESET}")
            elif is_print:
                print(f"{WARNING}Error occurred while creating HTML roles{RESET}")
            return ''
        s += '\n</table>'
        return s
    except BaseException as err:
        if print_errors:
            print(f"{WARNING}Error occurred while creating HTML roles: {err}{WARNING}")
        elif is_print:
            print(f"{WARNING}Error occurred while creating HTML roles{RESET}")
        return ''


def create_HTML_info(logs: list["LogInfo"] = None, print_errors = True) -> str:
    table_caption = ("\t<caption><h1><strong>"
                     "Таблица с информацией об игре"
                     "<br>"
                     "Table with information about game"
                     "</strong></h1></caption>\n")
    table_head = (f"\t<thead>\n"
                  f"\t\t<tr>\n"
                  f"\t\t\t<th style=\"color: {num_c}\">N</th>\n"
                  f"\t\t\t<th>Type of information</th>\n"
                  f"\t\t\t<th>Information-1</th>\n"
                  f"\t\t\t<th>Information-2 (reserve)</th>\n"
                  f"\t\t</tr>\n"
                  f"\t</thead>\n")
    table_body = ''
    try:
        if logs is not None:
            rows = []
            for log in logs:
                try:
                    row = ''
                    rows.append(row)
                except BaseException as err:
                    if print_errors:
                        print(f"{WARNING}Error occurred while creating HTML info: {err}{RESET}")
                    else:
                        print(f"{WARNING}Error occurred while creating HTML info{RESET}")
            table_body = "\t<tbody>\n" + '\n\t\t'.join(rows) + "\n\t</tbody>"
    except BaseException as err:
        if print_errors:
            print(f"{WARNING}Error occurred while creating HTML info: {err}{RESET}")
    table = "<table>\n" + table_caption + table_head + table_body + "\n</table>"
    return table


def create_HTML_logs_cards(logs, print_errors = True, is_print = True) -> str:
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
                        f"\t\t<th>Cards <font color=\"{pr_c}\">President</font> Said</th>"
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
            cooked = log.to_HTML()
            row = "\t<tr>" + number + cooked + '</tr>'
            rows.append(row)
        table_body += '\n'.join(rows)
        table_body += '\n</tbody>'
        table = "<table>\n" + table_caption + '\n' + table_head + '\n' + table_body + '\n</table>'
        return table
    except BaseException as err:
        if print_errors:
            print(f"{CRITICAL}Error occurred while creating HTML logs about cards: {err}{RESET}")
        elif is_print:
            print(f"{CRITICAL}Error occurred while creating HTML logs about cards{RESET}")
        return ''

def create_HTML_logs(path: str, logs: list["Log"], players: list["Player"] = None, roles: list[str] = None, logs_info = None) -> str:
    try:
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
                 th {
                     border: 3px """ + norm_c_cut + """ solid;
                 }
                 td {
                     border: 2px """ + norm_c_cut + """ solid;
                 }
             </style>
         </head>
         """

        try:
            table_roles = create_HTML_roles(players, roles)
        except BaseException as err:
            table_roles = ''
            print(f"Oops, something went wrong: {err}")
            print(f"{WARNING}Table of roles could not be created{RESET}")
        try:
            table_info = create_HTML_info(logs_info)
        except BaseException as err:
            table_info = ''
            print(f"Oops, something went wrong: {err}")
            print(f"{WARNING}Table with information could not be created{RESET}")
        try:
            table_logs = create_HTML_logs_cards(logs)
        except BaseException as err:
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
    except BaseException as err:
        print(f"Oops, something went wrong: {err}")
        print(f"{CRITICAL}HTML Table of logs could not be created!!!{RESET}")
        return ''
