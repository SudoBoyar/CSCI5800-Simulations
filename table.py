import random
import simpy
import simtime as st
import table_layouts


class Table(object):
    side_target = 200.00
    box_target = 1000.00

    def __init__(self, env, dice, capacity=12, scale=1):
        self.env = env

        self.stack_default = self.side_target * scale
        self.table_default = self.box_target * scale

        self.dice = dice
        self.point = None
        self.roll_event = self.env.event()

        self.bets = table_layouts.bets(self)

        self.capacity = capacity
        self.spots = simpy.Resource(env, capacity=capacity)
        self.players = [None for _ in range(capacity)]
        self.player_seats = {}

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

    def has_point(self):
        return self.point is not None

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
        available = [k for k, v in enumerate(self.players) if v is None]
        if len(available) == 0:
            raise RuntimeError('Table already full...')

        seat = available[self.player_placer.randint(0, len(available) - 1)]
        self.players[seat] = player
        self.player_seats[player.id] = seat

        if self.spots.count == 1:
            self.env.process(self.dummy_roll())

    def remove_player(self, player):
        seat = self.player_seats.pop(player.id)
        self.players[seat] = None

    def bet_request(self, player):
        if self.player_seats[player.id] < self.capacity/2:
            return self.left_dealer.request()
        elif self.capacity/2 <= self.player_seats[player.id] < self.capacity:
            return self.right_dealer.request()
        else:
            raise RuntimeError('Player sat at nonexistent seat')

    def dummy_roll(self):
        while self.spots.count > 0:
            yield self.env.timeout(st.seconds(30))
            roll = self.dice.roll()
            self.roll_event.success(roll)
            self.roll_event = self.env.event()

            if self.has_point():
                if roll == 7:
                    self.point = None
            elif not self.has_point():
                if roll in [4, 5, 6, 8, 9, 10]:
                    self.point = roll.total
