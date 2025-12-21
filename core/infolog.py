from __future__ import annotations

from core.HTML_colors import red_c, norm_c, purple_c, orange_c, yellow_c, num_c
from core.globs import INFO_LOGS
from core.standard_names_SH import X
from cli.user_color_settings import WARNING
from user_settings import IS_PRINT_SMALL_INFO


class InfoLog:
    def __init__(self, info_type: str, info_name, info1: object, info2: object = ''):
        self.info_type = str(info_type)
        self.info_name = str(info_name)
        self.info1 = str(info1)
        self.info2 = str(info2)

    def get_color_for_type(self, another_color: str = norm_c, num: int = None,
                           *, print_errors: bool = IS_PRINT_SMALL_INFO) -> str:
        match self.info_type:
            case X.ERROR:
                return red_c
            case X.WEAK_WARNING:
                return yellow_c
            case X.WARNING:
                return orange_c
            case X.INFO:
                return norm_c
            case X.DBG:
                return purple_c
            case _:
                if print_errors:
                    print(f"{WARNING}Unknown info_name type: {self.info_type}")
                    INFO_LOGS.append(
                        InfoLog(info_type=X.ERROR, info_name=f"{WARNING}Unknown info_name type: {self.info_type}",
                                info1=f'row= {num}, '
                                      f'info_name= {self.info_name}, <br>'
                                      f'additional_info= {self.info1}'))
                return another_color


    def to_HTML_row(self, num: int | None = None) -> str:
        info_num   = f'<td style="color: {num_c}"><b>{num}</b></td>'
        info_type  = f'<td style="color: {self.get_color_for_type()}"><b>{self.info_type}</b></td>\n'
        info_name  = f'<td><b>{self.info_name}</b></td>'
        info1      = f'<td>{self.info1}</td>'
        info2      = f'<td>{self.info2}</td>'
        row        = (f"\t\t<tr>\n"
                      f"\t\t\t{info_num}\n"
                      f"\t\t\t{info_type}\n"
                      f"\t\t\t{info_name}\n"
                      f"\t\t\t{info1}\n"
                      f"\t\t\t{info2}\n"
                      f"\t\t</tr>\n")
        return row
