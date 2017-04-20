from ManekiNeko.core.singleton.singleton import Singleton
from bot.core.state import State


class StateModel(metaclass=Singleton):

    NOW_STATE = State.STOP

    def check_training(self):
        return True if self.NOW_STATE == State.TRAINING else False

    def check_running(self):
        return True if self.NOW_STATE == State.RUNNING else False
