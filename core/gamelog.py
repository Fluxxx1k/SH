from __future__ import annotations

from Players.abstract_player import AbstractPlayer
from core.standard_classes import Cards

from core.standard_functions import color_clear


class GameLog:
    def __init__(self, prs: str | AbstractPlayer = '', cnc: str | AbstractPlayer = '', c_prs_got: str | Cards = '', c_prs_said: str | Cards = '', c_cnc_got: str | Cards = '', c_cnc_said: str | Cards = '', c_cnc_placed: str | Cards = '', c_prs_said_after: str | Cards = '', special: str = '', reserve: str = '',
                 is_cards: bool = True, is_president: bool = True, is_chancellor: bool = True):
        if isinstance(prs, AbstractPlayer):
            self.prs = prs.name
        elif isinstance(prs, str):
            self.prs = color_clear(prs)
        else:
            self.prs = str(prs)
            print(f"Strange president name ({type(prs)= }): {prs=}")

        if isinstance(cnc, AbstractPlayer):
            self.cnc = cnc.name
        elif isinstance(cnc, str):
            self.cnc = color_clear(cnc)
        else:
            self.cnc = str(cnc)
            print(f"Strange president name ({type(cnc)= }): {cnc=}")
        self.cpg = c_prs_got
        self.cps = c_prs_said
        self.ccg = c_cnc_got
        self.ccs = c_cnc_said
        self.ccp = c_cnc_placed
        self.cpsa = c_prs_said_after
        self.reserve = reserve
        self.special = special
        self.is_cards = is_cards
        self.is_president = is_president
        self.is_chancellor = is_chancellor
    def to_HTML_row(self) -> str:
        from core.HTML_colors import ch_c, pr_c, special_c, purple_c
        from core.HTML_logs import coloring_HTML_cards
        president = f'\t<td style="color: {pr_c if self.is_president else purple_c}"><b>{self.prs}</b></td>\n'
        chancellor = f'\t<td style="color: {ch_c if self.is_chancellor else purple_c}"><b>{self.cnc}</b></td>\n'
        c_prs_got = f"\t<td><b>{coloring_HTML_cards(self.cpg) if self.is_cards else self.cpg}</b></td>\n"
        c_prs_said = f"\t<td><b>{coloring_HTML_cards(self.cps) if self.is_cards else self.cps}</b></td>\n"
        c_cnc_got = f"\t<td><b>{coloring_HTML_cards(self.ccg) if self.is_cards else self.ccg}</b></td>\n"
        c_cnc_said = f"\t<td><b>{coloring_HTML_cards(self.ccs) if self.is_cards else self.ccs}</b></td>\n"
        c_cnc_placed = f"\t<td><b>{coloring_HTML_cards(self.ccp) if self.is_cards else self.ccp}</b></td>\n"
        c_prs_said_after = f"\t<td><b>{coloring_HTML_cards(self.cpsa) if self.is_cards else self.cpsa}</b></td>\n"
        special = f'\t<td style="color: {special_c}"><b>{self.special}</b></td>\n'
        row = president + chancellor + c_prs_got + c_prs_said + c_cnc_got + c_cnc_said + c_cnc_placed + c_prs_said_after + special
        return row
    def to_HTML_row_Website(self) -> str:
        from core.HTML_colors import ch_c, pr_c, special_c, purple_c
        from core.HTML_logs import coloring_HTML_cards
        president = f'\t<td style="color: {pr_c if self.is_president else purple_c}"><b>{self.prs}</b></td>\n'
        chancellor = f'\t<td style="color: {ch_c if self.is_chancellor else purple_c}"><b>{self.cnc}</b></td>\n'
        # c_prs_got = f"\t<td><b>{coloring_HTML_cards(self.cpg) if self.is_cards else self.cpg}</b></td>\n"
        c_prs_said = f"\t<td><b>{coloring_HTML_cards(self.cps) if self.is_cards else self.cps}</b></td>\n"
        # c_cnc_got = f"\t<td><b>{coloring_HTML_cards(self.ccg) if self.is_cards else self.ccg}</b></td>\n"
        c_cnc_said = f"\t<td><b>{coloring_HTML_cards(self.ccs) if self.is_cards else self.ccs}</b></td>\n"
        c_cnc_placed = f"\t<td><b>{coloring_HTML_cards(self.ccp) if self.is_cards else self.ccp}</b></td>\n"
        c_prs_said_after = f"\t<td><b>{coloring_HTML_cards(self.cpsa) if self.is_cards else self.cpsa}</b></td>\n"
        special = f'\t<td style="color: {special_c}"><b>{self.special}</b></td>\n'
        row = '\t<tr>' + president + chancellor + c_prs_said + c_cnc_said + c_cnc_placed + c_prs_said_after + special + '\t</tr>\n'
        return row