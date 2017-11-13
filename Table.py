import random
import simpy


class Table(object):
    side_target = 200.00
    box_target = 1000.00

    def __init__(self, env, dice, scale=1):
        """

        :param simpy.Environment env:
        :param dice:
        :param scale:
        """
        self.env = env

        self.stack_default = self.side_target * scale
        self.table_default = self.box_target * scale

        self.dice = dice
        self.point = None
        self.available_bets = []

        self.spots = simpy.Resource(env, capacity=12)

        self.left_dealer = simpy.Resource(env, capacity=1)
        self.left_stack = simpy.Container(env, capacity=float('inf'))
        self.left_stack.put(self.stack_default)

        self.right_dealer = simpy.Resource(env, capacity=1)
        self.right_stack = simpy.Container(env, capacity=float('inf'))
        self.right_stack.put(self.stack_default)

        self.boxman = simpy.Resource(env, capacity=1)
        self.table_stack = simpy.Container(env, capacity=float('inf'))
        self.table_stack.put(self.table_default)

        self.player_placer = random.Random(1234)
        self.left_players = []
        self.right_players = []

        self.transfers = []

        self.point_down_event = self.env.event()
        self.new_player_event = self.env.event()

    def table_accounting(self):
        while True:
            yield self.env.timeout(60*60)
            yield self.boxman.request()
            # request vault
            if self.table_stack.level > self.table_default:
                transfer_amount = self.table_stack.get(self.table_stack.level - self.table_default)
                # put amount in vault
                self.transfers.append((self.env.now, transfer_amount))
            elif self.table_stack.level < self.table_default:
                transfer_amount = self.table_default - self.table_stack.level
                # get amount from vault

    def add_player(self, player):
        if len(self.left_players) == 6:
            self.right_players.append(player.id)
        elif len(self.right_players) == 6:
            self.left_players.append(player.id)
        else:
            if self.player_placer.randint(0, 1) == 0:
                self.left_players.append(player.id)
            else:
                self.right_players.append(player.id)

    def bet_request(self, player):
        if player.id in self.left_players:
            return self.left_dealer.request()
        elif player.id in self.right_players:
            return self.right_dealer.request()
        else:
            # TODO Error Type
            raise ConnectionRefusedError()

