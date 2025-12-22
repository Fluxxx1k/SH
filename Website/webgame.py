from __future__ import annotations

import datetime

import user_settings
from core.abstractgame import AbstractGame
import random 
import random as rnd

from core.gamelog import GameLog
from core.infolog import InfoLog
from core.standard_names_SH import X
from user_settings import RED_WIN_NUM


class WebGame(AbstractGame):
    def take_move(self):
        if self.is_end():
            return self.is_end()
        i = (self.prs.num + 1)% self.globs.COUNT_PLAYERS
        while not self.accept_player(self.globs.PLAYERS[i]):
            i = (i + 1)% self.globs.COUNT_PLAYERS
        self.prs = self.globs.PLAYERS[i]
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
                self.saved_cards = []
            return 0
        self.skips = 0
        self.globs.PLAYERS[self.prs.num].chosen_gov(X.PRESIDENT)
        self.globs.PLAYERS[self.cnc.num].chosen_gov(X.CHANCELLOR)
        self.cards = self.take_random(3)
        cards_president_got = ''.join(self.cards)
        cards_president_said, self.cards, is_veto = self.prs.president(self.cards, self.cnc)
        cards_chancellor_got = ''.join(self.cards)
        cards_chancellor_said, cards_chancellor_placed = self.cnc.chancellor(self.cards, self.prs, cards_president_said, is_veto)
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
            self.globs.INFO_LOGS.append(InfoLog(X.ERROR, "Unknown chancellor card", f"ccp= {cards_chancellor_placed}, {self.prs= }, {self.cnc= }, {self.name}", f"WEB ({datetime.datetime.now().strftime(f'{user_settings.DATE_FORMAT} {user_settings.TIME_FORMAT}')}"))
        if cards_chancellor_placed != 'V':
            normal_logs.append(GameLog(prs=self.prs, cnc=self.cnc,
                                       c_prs_got=cards_president_got,
                                       c_prs_said=cards_president_said,
                                       c_prs_said_after=cards_president_said_after_chancellor,
                                       c_cnc_got=cards_chancellor_got,
                                       c_cnc_said=cards_chancellor_said,
                                       c_cnc_placed=cards_chancellor_placed))
        else:
            normal_logs.append(GameLog(prs=PLAYERS[pn], cnc=PLAYERS[cn],
                                       c_prs_got=c_prs_got, c_prs_said=cps, c_prs_said_after=cpsa,
                                       c_cnc_got=c_cnc_got, c_cnc_said=ccs, c_cnc_placed="",
                                       special="VETO"))



        
    