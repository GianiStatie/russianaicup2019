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
		player_view = self.gclient.get_raw_state()
		player_unit = self._get_player_unit(player_view)[0]
		state = self.extractor.get_game_state(player_view, player_unit)
		return state, player_view, player_unit

	def step(self, actions):
		"""
			inputs:  actions
			outputs: state, reward, done, info
		"""
		self.gclient.send_actions(actions)
		player_view = self.gclient.get_raw_state()
		if player_view is None:
			return [], -1, True, {}
		player_unit = self._get_player_unit(player_view)[0]
		state  = self.extractor.get_game_state(player_view, player_unit)
		info   = self._get_player_info(player_view, player_unit)
		reward = 0
		return state, reward, False, info

	def close(self):
		self.ghost.stop()

	def set_config(config_path):
		self.config_path = config_path

	def _get_player_unit(self, player_view):
		return [unit for unit in player_view.game.units \
						if unit.player_id == player_view.my_id]

	def _get_player_info(self, view, unit):
		weapon = unit.weapon
		info = {
			'health': unit.health,
			'game_ticks': view.game.current_tick,
			'weapon_typ': None if weapon is None else weapon.typ,
		}
		return info

	def _calculate_reward(self):
		pass

