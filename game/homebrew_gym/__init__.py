from game.homebrew_gym.homebrew_gym import HomebrewGym

def make(host, port, token, os_name, config_path=None, render_env=True):
	return HomebrewGym(host, port, token, os_name, config_path, render_env)