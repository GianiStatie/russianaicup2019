from game import game_host, game_client
import time

ml = game_host.make(os_name='macOS')
ml.start()

time.sleep(1)

host  = "127.0.0.1" 
port  = 31001 
token = "0000000000000000" 


cl = game_client.make(host, port, token)

time.sleep(5)

ml.stop()

time.sleep(1)

ml.start()
