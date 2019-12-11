from game.game_host.mac_game_host import MacGameHost
from game.game_host.win_game_host import WinGameHost

def make(os_name, config_path=None, render_env=True):
	if   'mac' in os_name.lower():
		return MacGameHost(config_path, render_env)
	elif 'win' in os_name.lower():
		return WinGameHost(config_path, render_env)
	else:
		pass