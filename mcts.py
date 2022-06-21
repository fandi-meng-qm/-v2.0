import gym
from gym import Env
from mcts_general.agent import MCTSAgent
from mcts_general.config import MCTSAgentConfig
from mcts_general.game import DiscreteGymGame


class DeadlyHotelEnv(Env):
    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode="human"):
        pass


class DeadlyHotelMCTS:
    __config = None
    __agent = None
    __game = None

    def __init__(self):
        self.__config = MCTSAgentConfig()
        self.__config.num_simulations = 200
        self.__agent = MCTSAgent(self.__config)
        self.__game = DiscreteGymGame(DeadlyHotelEnv())

    def run(self):
        times = 0
        kill = 0
        kill_without_detected = 0
        state = self.__game.reset()
        reward = 0
        done = False
        while True:
            action = self.__agent.step(self.__game, state, reward, done)
            self.__game.render(mode="console")
            print(action, reward)
            state, reward, done = self.__game.step(action)
            if done:
                times += 1
                if state[7] == 0:
                    kill += 1
                if len(state) == 9:
                    kill_without_detected += 1
                print('times: %d' % times)
                print('kills: %d' % kill)
                print('kill_without_detected: %d' % kill_without_detected)
                self.__game.reset()
        self.__game.close()
