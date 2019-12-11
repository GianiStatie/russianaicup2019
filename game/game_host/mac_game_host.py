from game.game_host.game_host import GameHost
import os
import time
from multiprocessing import Process

class MacGameHost(GameHost):
    def __init__(self, config_path=None, render_env=True):
        if config_path == None:
            self.config_path = './configs/config.json'
        self.render_env  = render_env

    def _start_app(self):
        if self.render_env:
            os.system(f'./aicup2019 --config {self.config_path}')
        else:
            os.system(f'./aicup2019 --config {self.config_path} --batch-mode')

    def _close_app(self):
        os.system('pkill aicup2019')

    def _reset_app(self):
        self._close_app()
        self._start_app()

    def start(self):
        p = Process(target=self._start_app)
        p.start()
        time.sleep(0.1) # wait for process to start

    def stop(self):
        p = Process(target=self._close_app)
        p.start()

    def reset(self):
        p = Process(target=self._reset_app)
        p.start()
        time.sleep(0.1) # wait for process to start