from __future__ import annotations

from typing import Literal, Iterable
import threading

from core.games.basegame import BaseGame
from core.players.abstract_player import AbstractPlayer
import time

check_interval = 10  # Check every 10 seconds
timeout = 600  # 10 minute timeout

class WebGame(BaseGame):
    def __init__(self, name: str, players: list[AbstractPlayer], description: str=''):
        super().__init__(name, players, description)

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
        """
        Wait for president action with 10-minute timeout
        Checks every 10 seconds for user input
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.has_action():
                return self.get_action()
            time.sleep(check_interval)
        
        if self.has_action():
            return self.get_action()
        raise TimeoutError("President action timeout")

    def chancellor(self, cards: str, prs: "AbstractPlayer", words, veto):
        """
        Wait for chancellor action with 10-minute timeout
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        

        while time.time() - start_time < timeout:
            if self.has_action():
                return self.get_action()
            time.sleep(check_interval)
        
        if self.has_action():
            return self.get_action()
        raise TimeoutError("Chancellor action timeout")

    def president_said_after_chancellor(self, *, cards: str, cnc: "AbstractPlayer", ccg: str, cps: str, ccs: str,
                                        ccp: str) -> str:
        """
        Wait for president response with 10-minute timeout
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        

        while time.time() - start_time < timeout:
            if self.has_action():
                return self.get_action()
            time.sleep(check_interval)
        
        if self.has_action():
            return self.get_action()
        raise TimeoutError("President response timeout")

    def check_cards(self, cards: str) -> str:
        """
        Wait for card check with 10-minute timeout
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        

        while time.time() - start_time < timeout:
            if self.has_action():
                return self.get_action()
            time.sleep(check_interval)
        
        if self.has_action():
            return self.get_action()
        raise TimeoutError("Card check timeout")

    def check_player(self) -> tuple[int, str]:
        """
        Wait for player check with 10-minute timeout
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        

        while time.time() - start_time < timeout:
            if self.has_action():
                return self.get_action()
            time.sleep(check_interval)
        
        if self.has_action():
            return self.get_action()
        raise TimeoutError("Player check timeout")

    def purge_another(self, purge_type: str, votes: dict[int, int] = None) -> int:
        """
        Wait for purge action with 10-minute timeout
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        

        while time.time() - start_time < timeout:
            if self.has_action():
                return self.get_action()
            time.sleep(check_interval)
        
        if self.has_action():
            return self.get_action()
        raise TimeoutError("Purge action timeout")

    def place_another(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        """
        Wait for placement action with 10-minute timeout
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        

        while time.time() - start_time < timeout:
            if self.has_action():
                return self.get_action()
            time.sleep(check_interval)
        
        if self.has_action():
            return self.get_action()
        raise TimeoutError("Placement action timeout")

    def choose_chancellor(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        """
        Wait for chancellor selection with 10-minute timeout
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        

        while time.time() - start_time < timeout:
            if self.has_action():
                return self.get_action()
            time.sleep(check_interval)
        
        if self.has_action():
            return self.get_action()
        raise TimeoutError("Chancellor selection timeout")

    def __init__(self, num: int, name: str, role: str):
        super().__init__(num, name, role)
        self._vote = None
        self._action = None
        

    def has_action(self) -> bool:
        """Check if player has submitted an action"""
        return self._action is not None
        
    def get_action(self):
        """Get and clear player's action"""
        action = self._action
        self._action = None
        return action
        
    def set_action(self, action):
        """Set player's action from web interface"""
        self._action = action

    def vote_for_pair(self, prs: 'AbstractPlayer', cnc: 'AbstractPlayer') -> Literal[-1, 0, 1]:
        """
        Wait for user vote with 60s timeout (defaults to PASS)
        Checks every 10 seconds for user input
        """
        start_time = time.time()
        timeout = 60  # 1 minute timeout


        while time.time() - start_time < timeout:
            if self.has_voted():
                return self.get_vote()
            time.sleep(check_interval)
        if self.has_voted():
            return self.get_vote()
        return 0  # Default to PASS if timeout