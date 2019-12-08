import model
from homebrew_gym import HomebrewGym 
import sys
import neat
import numpy as np

def distance_sqr(a, b):
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

def scale_state(state):
    max_val = np.amax(state)
    return state/max_val

def get_nearest_enemy(unit, game):
    nearest_enemy = min(
            filter(lambda u: u.player_id != unit.player_id, game.units),
            key=lambda u: distance_sqr(u.position, unit.position),
            default=None)
    return nearest_enemy

def get_aim(unit, nearest_enemy):
    aim = model.Vec2Double(0, 0)
    if nearest_enemy is not None:
        aim = model.Vec2Double(
            nearest_enemy.position.x - unit.position.x,
            nearest_enemy.position.y - unit.position.y)
    return aim

def format_action(raw_action, unit, game):
    direction = (raw_action[0]-0.5)*2
    speed = raw_action[1] * 5 # because holy trinity
    jump  = bool(round(raw_action[2]))
    shoot = bool(round(raw_action[3]))
    relod = bool(round(raw_action[4]))
    swapw = bool(round(raw_action[5]))
    plant = bool(round(raw_action[6]))
    nearest_enemy = get_nearest_enemy(unit, game)
    aim  = get_aim(unit, nearest_enemy)

    action = model.UnitAction(
             velocity=round(direction * speed),
             jump=jump,
             jump_down=not jump,
             aim=aim,
             shoot=shoot,
             reload=relod,
             swap_weapon=swapw,
             plant_mine=plant)

    return {unit.id: action}

def eval_genomes(genomes, config, render=False):
    for genome_id, genome in genomes:
        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        
        genome_fitenss = 0
        
        state = env.reset()

        for counter in range(5000):            
            state_ress = scale_state(state).flatten()

            raw_action = net.activate(state_ress)
            game = env.get_game()
            unit = env.get_player_unit()
            action = format_action(raw_action, unit, game)
            state, reward, done, info = env.step(action)
            
            if done: break

            genome_fitenss += reward
            
        print("Genome: ", genome_id, ", Fitness Achieved: ", genome_fitenss)
        genome.fitness = genome_fitenss         

if __name__ == "__main__":
    #Setup config
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')
    # creat population
    p = neat.Population(config)

    # add reporters so you can get some nice stats
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # save a check point file every 10 iterations
    p.add_reporter(neat.Checkpointer(10))

    # define environment
    host  = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port  = 31001 if len(sys.argv) < 3 else int(sys.argv[2])
    token = "0000000000000000" if len(sys.argv) < 4 else sys.argv[3]
    env = HomebrewGym(host, port, token)
    env.make()

    # this line runs the previous eval_genomes function. Once done, the best is set to winner
    winner = p.run(eval_genomes)

    #saves a pickle file of the winning genome.
    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)
