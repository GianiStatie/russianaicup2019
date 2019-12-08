import model
import math
import numpy as np

class StateExtractor():
    def __init__(self):
        self.game_bg = None

    def _init_background(self, player_view):
        self.bg_width  = len(player_view.game.level.tiles)
        self.bg_height = len(player_view.game.level.tiles[0])
        self.game_bg   = np.zeros((self.bg_height, self.bg_width))
    
        for j, row in enumerate(player_view.game.level.tiles):
            for i, tile in enumerate(row):
                if   str(tile) == 'Tile.EMPTY':
                    self.game_bg[i][j] = 0
                elif str(tile) == 'Tile.WALL':
                    self.game_bg[i][j] = 1
                elif str(tile) == 'Tile.PLATFORM':
                    self.game_bg[i][j] = 2
                elif str(tile) == 'Tile.LADDER':
                    self.game_bg[i][j] = 3
                elif str(tile) == 'Tile.JUMP_PAD':
                    self.game_bg[i][j] = 4

    def get_game_state(self, player_view, player_unit):
        game_state = self.get_background(player_view)
        game_state = self.add_loot_boxes(game_state, player_view)
        game_state = self.add_player_loc(game_state, player_view, player_unit)
        game_state = np.flip(game_state, axis = 0)
        return game_state
 
    def get_background(self, player_view):
        if self.game_bg is None:
            self._init_background(player_view)
        return self.game_bg.copy()

    def add_loot_boxes(self, game_state, player_view):
        for element in player_view.game.loot_boxes:
            loot_box_y = int(round(element.position.y))
            loot_box_x = int(round(element.position.x)) if element.position.x <= self.bg_width/2 \
                                                        else int(round(element.position.x)-1)
            lb_height = math.ceil(element.size.y)
            lb_length = math.ceil(element.size.x)
            if   isinstance(element.item, model.Item.HealthPack):
                game_state[loot_box_y : loot_box_y + lb_height, loot_box_x : loot_box_x + lb_length] = 5
            elif isinstance(element.item, model.Item.Mine):
                game_state[loot_box_y : loot_box_y + lb_height, loot_box_x : loot_box_x + lb_length] = 6
            elif isinstance(element.item, model.Item.Weapon):
                if   element.item.weapon_type == model.WeaponType.PISTOL:
                    game_state[loot_box_y : loot_box_y + lb_height, loot_box_x : loot_box_x + lb_length] = 7
                elif element.item.weapon_type == model.WeaponType.ASSAULT_RIFLE:
                    game_state[loot_box_y : loot_box_y + lb_height, loot_box_x : loot_box_x + lb_length] = 8
                elif element.item.weapon_type == model.WeaponType.ROCKET_LAUNCHER:
                    game_state[loot_box_y : loot_box_y + lb_height, loot_box_x : loot_box_x + lb_length] = 9
        return game_state

    def add_player_loc(self, game_state, player_view, player_unit):
        for unit in player_view.game.units:
            unit_y = int(round(unit.position.y))
            unit_x = int(round(unit.position.x)) if unit.position.x <= self.bg_width/2 \
                                                 else int(round(unit.position.x)-1)
            unit_height = math.ceil(unit.size.y)
            unit_length = math.ceil(unit.size.x)
            if unit.player_id != player_unit.player_id:
                game_state[unit_y : unit_y + unit_height, unit_x : unit_x + unit_length] = 10
            else:
                game_state[unit_y : unit_y + unit_height, unit_x : unit_x + unit_length] = 11
        return game_state
            
