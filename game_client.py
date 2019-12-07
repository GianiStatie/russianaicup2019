import model
from src.stream_wrapper import StreamWrapper
import socket

class GameClient():
    def __init__(self, host, port, token):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.socket.connect((host, port))
        socket_stream = self.socket.makefile('rwb')
        self.reader = StreamWrapper(socket_stream)
        self.writer = StreamWrapper(socket_stream)
        self.writer.write_string(token)
        self.writer.flush()

    def get_raw_state(self):
        message = model.ServerMessageGame.read_from(self.reader)
        return message.player_view

    def send_actions(self, actions):
        model.PlayerMessageGame.ActionMessage(
                model.Versioned(actions)).write_to(self.writer)
        self.writer.flush()
