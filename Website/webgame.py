from __future__ import annotations

import datetime
from typing import Literal

import user_settings
from Players.abstract_player import AbstractPlayer
from core.HTML_colors import purple_c, pr_c
from core.HTML_logs import color_of_HTML_roles
from core.abstractgame import AbstractGame
import random as rnd

from core.gamelog import GameLog
from core.infolog import InfoLog
from core.standard_names_SH import X
from user_settings import RED_WIN_NUM


class WebGame(AbstractGame):
    def choose_next_president(self) -> AbstractPlayer:
        i = (self.prs.num + 1) % self.globs.COUNT_PLAYERS
        while not self.accept_player(self.globs.PLAYERS[i]):
            i = (i + 1) % self.globs.COUNT_PLAYERS
        return self.globs.PLAYERS[i]

    def president_chancellor_cards(self) -> Literal[-1, 0, 1]:
        self.cards = self.take_random(3)
        cards_president_got = ''.join(self.cards)
        cards_president_said, self.cards, is_veto = self.prs.president(self.cards, self.cnc)
        cards_chancellor_got = ''.join(self.cards)
        cards_chancellor_said, cards_chancellor_placed = self.cnc.chancellor(''.join(self.cards), self.prs,
                                                                             cards_president_said, is_veto)
        cards_president_said_after_chancellor = self.prs.president_said_after_chancellor(cnc=self.cnc,
                                                                                         cards=cards_president_got,
                                                                                         ccg=cards_chancellor_got,
                                                                                         ccp=cards_chancellor_placed,
                                                                                         cps=cards_president_said,
                                                                                         ccs=cards_chancellor_said)
        if cards_chancellor_placed == 'B':
            self.globs.BLACK += 1
            if self.globs.BLACK == user_settings.BLACK_WIN_NUM:
                if self.prs is not None:
                    self.globs.PLAYERS[self.prs.num].degov()
                if self.cnc is not None:
                    self.globs.PLAYERS[self.cnc.num].degov()
                return 1
            self.do_with_black()
        elif cards_chancellor_placed == 'R':
            self.globs.RED += 1
            if self.globs.RED == RED_WIN_NUM:
                if self.prs is not None:
                    self.globs.PLAYERS[self.prs.num].degov()
                if self.cnc is not None:
                    self.globs.PLAYERS[self.cnc.num].degov()
                return -1
        elif (cards_chancellor_placed in {"VETO", "X", "V"} and self.globs.BLACK >= user_settings.VETO_NUM_BLACK):
            cards_chancellor_placed = "V"
        else:
            self.globs.INFO_LOGS.append(InfoLog(X.ERROR, "Unknown chancellor card",
                                                f"ccp= {cards_chancellor_placed}, {self.prs= }, {self.cnc= }, {self.name}",
                                                f"WEB ({datetime.datetime.now().strftime(f'{user_settings.DATE_FORMAT} {user_settings.TIME_FORMAT}')}"))
        if cards_chancellor_placed != 'V':
            self.globs.GAME_LOGS.append(GameLog(prs=self.prs, cnc=self.cnc,
                                                c_prs_got=cards_president_got,
                                                c_prs_said=cards_president_said,
                                                c_prs_said_after=cards_president_said_after_chancellor,
                                                c_cnc_got=cards_chancellor_got,
                                                c_cnc_said=cards_chancellor_said,
                                                c_cnc_placed=cards_chancellor_placed))
        else:
            self.globs.GAME_LOGS.append(GameLog(prs=self.prs, cnc=self.cnc,
                                                c_prs_got=cards_president_got, c_prs_said=cards_president_said,
                                                c_prs_said_after=cards_president_said_after_chancellor,
                                                c_cnc_got=cards_chancellor_got, c_cnc_said=cards_chancellor_said,
                                                c_cnc_placed="",

                                            special="VETO"))
        return 0

    def placing_card(self, ccp):
        if ccp == 'B':
            self.globs.BLACK += 1
            self.checks += 1
            if self.globs.BLACK == user_settings.BLACK_WIN_NUM:
                if self.prs is not None:
                    self.globs.PLAYERS[self.prs.num].degov()
                if self.cnc is not None:
                    self.globs.PLAYERS[self.cnc.num].degov()
                return 1
        elif ccp == 'R':
            self.globs.RED += 1
            if self.globs.RED == RED_WIN_NUM:
                if self.prs is not None:
                    self.globs.PLAYERS[self.prs.num].degov()
                if self.cnc is not None:
                    self.globs.PLAYERS[self.cnc.num].degov()
                return -1
        else:
            print(f"WTH?!!!! {ccp} isn't 'B' or 'R'")
    def take_move(self) -> Literal[-1, 0, 1]:
        if self.is_end():
            return self.is_end()
        self.prs = self.choose_next_president()
        self.cnc = self.globs.PLAYERS[self.prs.choose_chancellor(self.globs.PLAYERS)]
        vote_sum = sum([player.vote_for_pair(self.prs, self.cnc) for player in self.players])
        if vote_sum <= 0:
            self.skips += 1
            if self.skips % user_settings.ANARCHY_SKIP_NUM == 0:
                if self.saved_cards:
                    self.globs.GAME_LOGS.append(GameLog(special="Cards was shuffled!"))
                    ccp = rnd.sample(self.saved_cards, k=1)[0]
                else:
                    ccp = self.take_random(1)[0]
                self.globs.GAME_LOGS.append(GameLog(prs="ANARCHY", cnc="ANARCHY",      
                                                    c_cnc_placed=ccp, special=f"({self.skips} skips)",
                                                    is_chancellor=False, is_president=False))
                self.placing_card(ccp)
                self.saved_cards = []
            return 0
        self.skips = 0
        self.globs.PLAYERS[self.prs.num].chosen_gov(X.PRESIDENT)
        self.globs.PLAYERS[self.cnc.num].chosen_gov(X.CHANCELLOR)
        return self.president_chancellor_cards()

    def do_with_black(self) -> Literal[-1, 0, 1]:
        match self.checks:
            case 1:
                return self.do_with_1_black()
            case 2:
                return self.do_with_2_black()
            case 3:
                return self.do_with_3_black()
            case 4:
                return self.do_with_4_black()
            case 5:
                return self.do_with_5_black()
            case _:
                self.globs.INFO_LOGS.append(InfoLog(X.ERROR, "Unknown checks", f"{self.checks= }", f"WEB ({datetime.datetime.now().strftime(f'{user_settings.DATE_FORMAT} {user_settings.TIME_FORMAT}')}"))
                return 0
    def do_with_1_black(self) -> Literal[-1, 0, 1]:
        self.saved_cards = self.take_random(3)
        cards_president_said_after_check = self.prs.check_cards(''.join(self.saved_cards))
        self.globs.GAME_LOGS.append(GameLog(prs=self.prs,
                                            c_prs_got=''.join(self.saved_cards),
                                            c_prs_said=cards_president_said_after_check,
                                            special="Card check"))
        self.checks = 2
        return 0
    def do_with_2_black(self) -> Literal[-1, 0, 1]:
        president_checked, color_president_checked = self.prs.check_player()
        if color_president_checked != self.globs.PLAYERS[president_checked].color:
            self.globs.PLAYERS[president_checked].black.add(self.prs.num)
        self.globs.GAME_LOGS.append(
            GameLog(prs=self.prs, cnc=self.cnc,
                    special=f"[<font color='{pr_c}'>{self.prs}</font>] said, that color of [<font color='{purple_c}'>{self.cnc}</font>] is <font color='{color_of_HTML_roles(color_president_checked)}'>{color_president_checked}</font>",
                    is_chancellor=False))
        self.checks = 3
        return 0
    def do_with_3_black(self) -> Literal[-1, 0, 1]:
        self.globs.GULAG = self.prs.purge_another(X.GULAG)
        self.globs.GAME_LOGS.append(
            GameLog(prs=self.prs, special="In gulag", is_cards=False, is_chancellor=False))
        self.globs.PLAYERS[self.globs.GULAG].purge(X.GULAG)
        if self.globs.GULAG == self.globs.HITLER:
            self.globs.GAME_LOGS.append(GameLog(prs=self.prs, special="Hitler caput", is_cards=False, is_chancellor=False))
            self.globs.HIT_CAPUT = True
            self.globs.GAME_LOGS.append(GameLog(prs=self.prs, special="Game over", is_cards=False, is_chancellor=False))
            return 1
        else:
            self.globs.GIT_NOT.add(self.globs.GULAG)
        self.checks = 4
        return 0


    def do_with_4_black(self) -> Literal[-1, 0, 1]:
        self.checks = 5
        return 0
    def do_with_5_black(self) -> Literal[-1, 0, 1]:
        self.globs.KILLED = self.prs.purge_another(X.SHOUT)
        if self.globs.GULAG == self.globs.KILLED:
            self.globs.GULAG = None
        self.globs.PLAYERS[self.globs.KILLED].purge(X.KILLED)
        self.globs.GAME_LOGS.append(GameLog(prs=self.prs, special=f"Killed", is_cards=False, is_chancellor=False))
        if self.globs.KILLED == self.globs.HITLER:
            self.globs.GAME_LOGS.append(GameLog(prs=self.prs, special="Hitler caput", is_cards=False, is_chancellor=False))
            self.globs.HIT_CAPUT = True
            self.globs.GAME_LOGS.append(GameLog(prs=self.prs, special="Game over", is_cards=False, is_chancellor=False))
            return 1
        else:
            self.globs.GIT_NOT.add(self.globs.KILLED)
        self.checks = 5
        return 0

