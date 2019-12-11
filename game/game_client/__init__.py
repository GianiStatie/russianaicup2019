from game.game_client.game_client import GameClient

def make(host, port, token):
	return GameClient(host, port, token)