import os
from multiprocessing import Process

class MacGameHost():
    def __init__(self, config_path=None):
        if config_path == None:
            self.config_path = './config.json'

    def _start_app(self):
        os.system(f'./aicup2019 --config {self.config_path}')

    def _close_app(self):
        os.system('pkill aicup')

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
    # time.sleep(2)
    # ml.reset()
    # time.sleep(2)
    # ml.stop()