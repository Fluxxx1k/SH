from core.players.abstract_player import AbstractPlayer
from core.standard_names_SH import X

class WebPlayer(AbstractPlayer):
    def __init__(self, num: int, name: str, role: str, socket_id: str):
        super().__init__(num=num, name=name, role=role)
        self.socket_id = socket_id
        self.pending_action = None
        self.action_result = None

    def president(self, cards: list[str], cnc: AbstractPlayer):
        self.pending_action = {
            'type': 'president_action',
            'cards': cards,
            'chancellor': cnc.name
        }
        # Wait for response from frontend
        while self.action_result is None:
            continue
        result = self.action_result
        self.action_result = None
        return result['words'], result['to_cnc'], result['veto']

    def chancellor(self, cards: str, prs: AbstractPlayer, words: str, veto: bool):
        self.pending_action = {
            'type': 'chancellor_action',
            'cards': cards,
            'president': prs.name,
            'words': words,
            'veto_possible': veto
        }
        # Wait for response from frontend
        while self.action_result is None:
            continue
        result = self.action_result
        self.action_result = None
        return result['words'], result['placed']

    def vote_for_pair(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> int:
        self.pending_action = {
            'type': 'vote_action',
            'president': prs.name,
            'chancellor': cnc.name
        }
        # Wait for response from frontend
        while self.action_result is None:
            continue
        result = self.action_result
        self.action_result = None
        return result['vote']

    def check_player(self) -> tuple[int, str]:
        self.pending_action = {'type': 'check_player_action'}
        while self.action_result is None:
            continue
        result = self.action_result
        self.action_result = None
        return result['player_num'], result['color']

    def purge_another(self, purge_type: str, votes: dict[int, int] = None) -> int:
        self.pending_action = {
            'type': 'purge_action',
            'purge_type': purge_type
        }
        while self.action_result is None:
            continue
        result = self.action_result
        self.action_result = None
        return result['target']