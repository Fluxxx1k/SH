from typing import Literal, Iterable
import threading

from core.games.basegame import BaseGame
from core.players.abstract_player import AbstractPlayer
from core.players.player import Player
import time

class WebGame(BaseGame):
    def __init__(self, game_data):
        super().__init__(game_data)
        self.players = [WebPlayer(p) for p in game_data['players']]
    def voting(self):
        return sum(self.collect_votes())

    def voting_web(self):
        """
        Perform voting process with parallel vote collection.
        Returns the voting results.
        """
        votes = self.collect_votes()
        
        # Calculate total votes
        total_votes = sum(votes.values())
        
        # Return voting results
        return {
            'votes': votes,
            'total': total_votes,
            'passed': total_votes > 0
        }

    def collect_votes(self):
        """
        Collect votes from all players in parallel.
        Returns a dictionary of {player_id: vote_value}
        """
        votes = {}
        threads = []
        
        def get_player_vote(player):
            vote = player.get_vote()
            votes[player.id] = vote
            
        for player in self.players:
            thread = threading.Thread(target=get_player_vote, args=(player,))
            thread.start()
            threads.append(thread)
            
        for thread in threads:
            thread.join()
            
        return votes


class WebPlayer(AbstractPlayer):
    def president(self, cards: str | list[str], cnc: "AbstractPlayer"):
        pass

    def chancellor(self, cards: str, prs: "AbstractPlayer", words, veto):
        pass

    def president_said_after_chancellor(self, *, cards: str, cnc: "AbstractPlayer", ccg: str, cps: str, ccs: str,
                                        ccp: str) -> str:
        pass

    def check_cards(self, cards: str) -> str:
        pass

    def check_player(self) -> tuple[int, str]:
        pass

    def purge_another(self, purge_type: str, votes: dict[int, int] = None) -> int:
        pass

    def place_another(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        pass

    def choose_chancellor(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        pass

    def __init__(self, player_data):
        super().__init__(player_data)
        self._vote = None
        
    def has_voted(self) -> bool:
        """Check if player has submitted a vote"""
        return self._vote is not None
        
    def get_vote(self) -> Literal[-1, 0, 1]:
        """Get player's vote (1=YES, -1=NO, 0=PASS)"""
        vote = self._vote
        self._vote = None
        return vote
        
    def set_vote(self, vote: Literal[-1, 0, 1]):
        """Set player's vote from web interface"""
        self._vote = vote

    def vote_for_pair(self, prs: 'AbstractPlayer', cnc: 'AbstractPlayer') -> Literal[-1, 0, 1]:
        """
        Wait for user vote with 60s timeout (defaults to PASS)
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        timeout = 60  # 1 minute timeout
        check_interval = 10  # Check every 10 seconds

        while time.time() - start_time < timeout:
            if self.has_voted():
                return self.get_vote()
            time.sleep(check_interval)
        if self.has_voted():
            return self.get_vote()
        return 0  # Default to PASS if timeout