from game_host import MacGameHost
from game_client import GameClient

class HomebrewGym():
	def __init__(self, host, port, token, config_path=None):
		self.host  = host
		self.port  = port
		self.token = token
		self.config_path = config_path

	def make(self):
		self.ghost   = MacGameHost(self.config_path)
		self.gclient = GameClient(self.host, self.port, self.token)

	def reset(self):
		self.ghost.reset()
		player_view = self.gclient.get_raw_state()
		# TODO use function from Ana in order to create state 
		#      from player view
		return state

	def step(self, actions):
		"""
			inputs:  actions
			outputs: state, reward, done, info
		"""
		# by sending the actions we obtain new game states
		self.gclient.send_actions(actions)
		player_view = self.gclient.get_raw_state()
		if player_view is None:
			return [], -1, True, None
		return state, reward, done, info

	def close(self):
		self.ghost.stop()

	def set_config(config_path):
		self.config_path = config_path

	def _calculate_state(self):
		pass

	def _calculate_reward(self):
		pass

