import model
from game import homebrew_gym
import sys
import neat
import numpy as np
import pickle

def scale_state(state):
    max_val = np.amax(state)
    return state/max_val

def get_aim(unit, nearest_enemy):
    aim = model.Vec2Double(0, 0)
    if nearest_enemy is not None:
        aim = model.Vec2Double(
            nearest_enemy.position.x - unit.position.x,
            nearest_enemy.position.y - unit.position.y)
    return aim

def format_action(raw_action, unit):
    direction = (raw_action[0]-0.5)*2
    speed = raw_action[1] * 5 # because holy trinity
    jump  = bool(round(raw_action[2]))
    shoot = bool(round(raw_action[3]))
    # relod = bool(round(raw_action[4]))
    # swapw = bool(round(raw_action[5]))
    # plant = bool(round(raw_action[6]))
    nearest_enemy = env.get_nearest_enemy()
    aim  = get_aim(unit, nearest_enemy)

    action = model.UnitAction(
             velocity=round(direction * speed),
             jump=jump,
             jump_down=not jump,
             aim=aim,
             shoot=shoot,
             reload=False,
             swap_weapon=False,
             plant_mine=False)

    return {unit.id: action}

def eval_genomes(genomes, config, render=False):
    for genome_id, genome in genomes:
        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        
        genome_fitenss = 0
        
        state = env.reset()

        for counter in range(1000):            
            state_ress = scale_state(state).flatten()

            raw_action = net.activate(state_ress)
            unit   = env.get_player_unit()
            action = format_action(raw_action, unit)
            state, reward, done, info = env.step(action)
            
            if done: break

            genome_fitenss += reward
            
        print("Genome: ", genome_id, ", Fitness Achieved: ", genome_fitenss)
        genome.fitness = genome_fitenss         

if __name__ == "__main__":
    #Setup config
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         './configs/config-feedforward')
    # creat population
    p = neat.Population(config)

    # add reporters so you can get some nice stats
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # save a check point file every 10 iterations
    p.add_reporter(neat.Checkpointer(10, 
                            filename_prefix='./checkpoints/neat-checkpoint-'))

    # # restore checkpoint
    # p = neat.Checkpointer.restore_checkpoint('./checkpoints/neat-checkpoint-78')

    # define environment
    host  = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port  = 31001 if len(sys.argv) < 3 else int(sys.argv[2])
    token = "0000000000000000" if len(sys.argv) < 4 else sys.argv[3]
    env = homebrew_gym.make(host, port, token, os_name='MacOS', render_env=False)

    # this line runs the previous eval_genomes function. Once done, the best is set to winner
    winner = p.run(eval_genomes)

    #saves a pickle file of the winning genome.
    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)

