from HTML_colors import red_c, norm_c, purple_c, orange_c, yellow_c
from globs import INFO_LOGS
from standard_names_SH import X
from user_color_settings import WARNING
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


    def to_HTML_row(self, num: int = None) -> str:
        row: str
        info_type       = f'\t\t\t<td style="color: {self.get_color_for_type()}"><b>{self.info_type}</b></td>\n'
        info_name           = f'\t\t\t<td><b>{self.info_name}</b></td>\n'
        info1 = f'\t\t\t<td>{self.info1}</td>\n'
        info2 = f'\t\t\t<td>{self.info2}</td>\n'
        row = f"\t\t<tr>\n{info_type}{info_name}{info1}{info2}</tr>\n"
        return row
