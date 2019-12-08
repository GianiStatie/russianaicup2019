from homebrew_gym import HomebrewGym 
from strategies.my_strategy import MyStrategy
import sys

if __name__ == "__main__":
    host  = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port  = 31001 if len(sys.argv) < 3 else int(sys.argv[2])
    token = "0000000000000000" if len(sys.argv) < 4 else sys.argv[3]

    strategy = MyStrategy()
    env = HomebrewGym(host, port, token)

    env.make()

    state, player_view, player_unit = env.reset()
    # print(state)
    for i in range(500):
	    actions = {}
	    actions[player_unit.id] = strategy.get_action(
	                        player_unit, player_view.game)
	    player_view, player_unit, info = env.step(actions)
	    print(info)

    env.close()  

    