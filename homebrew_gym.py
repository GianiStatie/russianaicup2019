from game_host import MacGameHost
from game_client import GameClient
from src.state_extractor import StateExtractor
import time

class HomebrewGym():
    def __init__(self, host, port, token, config_path=None):
        self.host  = host
        self.port  = port
        self.token = token
        self.config_path = config_path

        self.extractor = StateExtractor()

    def make(self):
        self.ghost = MacGameHost(self.config_path)
        self.ghost.start()
        time.sleep(1)
        self.gclient = GameClient(self.host, self.port, self.token)

    def reset(self):
        self.ghost.reset()
        time.sleep(1)
        self.gclient = GameClient(self.host, self.port, self.token)
        self.player_view = self.gclient.get_raw_state()
        self.player_unit = self._get_player_unit()[0]
        state = self.extractor.get_game_state(self.player_view, self.player_unit)
        return state

    def step(self, actions):
        """
            inputs:  actions
            outputs: state, reward, done, info
        """
        self.gclient.send_actions(actions)
        self.player_view = self.gclient.get_raw_state()
        if self.player_view is None:
            return [], -1, True, {}
        self.player_unit = self._get_player_unit()[0]
        state  = self.extractor.get_game_state(self.player_view, self.player_unit)
        info   = self._get_player_info()
        reward = self._calculate_reward(info)
        return state, reward, False, info

    def close(self):
        self.ghost.stop()

    def get_player_view(self):
        return self.player_view

    def get_player_unit(self):
        return self.player_unit

    def set_config(config_path):
        self.config_path = config_path

    def distance_sqr(self, a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

    def get_distance(self, a, b):
        return ((a.x - b.x) ** 2)**1/2

    def get_nearest_enemy(self):
        nearest_enemy = min(
            filter(lambda u: u.player_id != self.player_unit.player_id, self.player_view.game.units),
            key=lambda u: self.distance_sqr(u.position, self.player_unit.position),
            default=None)
        return nearest_enemy

    def _get_player_unit(self):
        return [unit for unit in self.player_view.game.units \
                        if unit.player_id == self.player_view.my_id]

    def _get_player_info(self):
        weapon = self.player_unit.weapon
        score  = [player.score for player in self.player_view.game.players \
                        if player.id == self.player_unit.player_id][0]
        info   = {
            'score': score,
            'health': self.player_unit.health,
            'game_ticks': self.player_view.game.current_tick,
            'weapon_typ': None if weapon is None else weapon.typ,
        }
        return info

    def _calculate_reward(self, info):
        nearest_enemy  = self.get_nearest_enemy()
        distance_to_ne = self.get_distance(nearest_enemy.position, self.player_unit.position)
        return info['score']/info['game_ticks'] + 0.1*(1 - distance_to_ne/688)

