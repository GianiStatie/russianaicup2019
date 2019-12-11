from game.game_host.game_host import GameHost
import os
from multiprocessing import Process

class WinGameHost(GameHost):
    def __init__(self, config_path=None, render_env=True):
        if config_path == None:
            self.config_path = './configs/config.json'
        self.render_env  = render_env

    def _start_app(self):
        if self.render_env:
            os.system(f'cd ./game; aicup2019.exe --config {self.config_path}')
        else:
            os.system('cd ./game')
            os.system(f'cd ./game; aicup2019.exe --config {self.config_path} --batch-mode')

    def _close_app(self):
        os.system('taskkill /im aicup2019.exe')

    def _reset_app(self):
        self._close_app()
        self._start_app()

    def start(self):
        p = Process(target=self._start_app)
        p.start()

    def stop(self):
        p = Process(target=self._close_app)
        p.start()

    def reset(self):
        p = Process(target=self._reset_app)
        p.start()

# if __name__ == '__main__':
#     ml = MacGameHost()
#     ml.start()
#     # time.sleep(2)
#     # ml.reset()
#     # time.sleep(2)
#     # ml.stop()