import model
from src.stream_wrapper import StreamWrapper
from src.debug import Debug
from strategies.my_strategy import MyStrategy
import socket
import sys
import numpy as np
import math



class Runner:
    def __init__(self, host, port, token):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.socket.connect((host, port))
        socket_stream = self.socket.makefile('rwb')
        self.reader = StreamWrapper(socket_stream)
        self.writer = StreamWrapper(socket_stream)
        self.token = token
        self.writer.write_string(self.token)
        self.writer.flush()
    
    def run(self):
        iteration = 0
        strategy = MyStrategy()
        debug = Debug(self.writer)

        width = 0
        height = 0
        game_matrix = np.zeros((height, width))
        f = open("myf.txt","w+")
        while True:
            message = model.ServerMessageGame.read_from(self.reader)
            if message.player_view is None:
                break
            player_view = message.player_view
            actions = {}
            for unit in player_view.game.units:
                if unit.player_id == player_view.my_id:
                    actions[unit.id] = strategy.get_action(
                        unit, player_view.game, debug)
            model.PlayerMessageGame.ActionMessage(
                model.Versioned(actions)).write_to(self.writer)

            width = len(player_view.game.level.tiles)
            height = len(player_view.game.level.tiles[0])
            
            if iteration == 0:
                width  = len(player_view.game.level.tiles)
                height = len(player_view.game.level.tiles[0])
                game_matrix = np.zeros((height, width))
            
                for j, row in enumerate(player_view.game.level.tiles):
                    for i, tile in enumerate(row):
                        if str(tile) == 'Tile.EMPTY':
                            game_matrix[i][j] = 0
                        elif str(tile) == 'Tile.WALL':
                            game_matrix[i][j] = 1
                        elif str(tile) == 'Tile.PLATFORM':
                            game_matrix[i][j] = 2
                        elif str(tile) == 'Tile.LADDER':
                            game_matrix[i][j] = 3
                        elif str(tile) == 'Tile.JUMP_PAD':
                            game_matrix[i][j] = 4
                        elif str(tile) == 'MY_POSITION':
                            game_matrix[i][j] = 5

                for element in player_view.game.loot_boxes:
                    loot_box_x = int(round(element.position.x)) if element.position.x <= width/2 else int(round(element.position.x)-1)
                    loot_box_y = int(round(element.position.y))
                    lb_length = math.ceil(element.size.x)
                    lb_height = math.ceil(element.size.y)
                    if isinstance(element.item, model.Item.Weapon):
                        if element.item.weapon_type == model.WeaponType.PISTOL:
                            game_matrix[loot_box_y : loot_box_y + lb_height,loot_box_x : loot_box_x + lb_length] = 6
                        elif element.item.weapon_type == model.WeaponType.ASSAULT_RIFLE:
                            game_matrix[loot_box_y : loot_box_y + lb_height,loot_box_x : loot_box_x + lb_length] = 7
                        elif element.item.weapon_type == model.WeaponType.ROCKET_LAUNCHER:
                            game_matrix[loot_box_y : loot_box_y + lb_height,loot_box_x : loot_box_x + lb_length] = 8
                    elif isinstance(element.item, model.Item.HealthPack):
                        game_matrix[loot_box_y : loot_box_y + lb_height,loot_box_x : loot_box_x + lb_length] = 9
                    elif isinstance(element.item, model.Item.Mine):
                        game_matrix[loot_box_y : loot_box_y + lb_height,loot_box_x : loot_box_x + lb_length] = 10
                for u in player_view.game.units:
                    enemy_x = int(round(u.position.x)) if u.position.x <= width/2 else int(round(u.position.x)-1)
                    enemy_y = int(round(u.position.y))
                    enemy_length = math.ceil(u.size.x)
                    enemy_height = math.ceil(u.size.y)
                    if u.player_id != unit.player_id:
                        game_matrix[enemy_y : enemy_y + enemy_height, enemy_x : enemy_x + enemy_length] = 11
                    else:
                        game_matrix[enemy_y : enemy_y + enemy_height, enemy_x : enemy_x + enemy_length] = 12
                            
                       
                    
                game_matrix = np.flip(game_matrix, axis = 0)
                np.savetxt('myf.txt', game_matrix, delimiter=' ', fmt='%d')
                break

            
            self.writer.flush()

        


if __name__ == "__main__":
    host = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port = 31001 if len(sys.argv) < 3 else int(sys.argv[2])
    token = "0000000000000000" if len(sys.argv) < 4 else sys.argv[3]
    Runner(host, port, token).run()
