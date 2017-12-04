from simtime import seconds, pretty_time


class Player(object):
    def __init__(self, table, id, play_time, wait_time):
        self.table = table
        self.spot = None

        self.id = id
        self.play_time = play_time
        self.wait_time = wait_time
        self.t_arrival = None
        self.t_seated = None
        self.t_departure = None

        self.shooter_count = 0
        self.points_hit = []

    def __str__(self):
        return "Player({id})".format(id=self.id)

    def arrive(self, env):
        self.t_arrival = env.now
        print(self, " arrived at ", pretty_time(env.now))

        spot_request = self.table.spots.request()
        result = yield spot_request | env.timeout(self.wait_time)

        if spot_request in result:
            # Seated at the table
            self.spot = spot_request
            self.t_seated = env.now
            wait = self.t_seated - self.t_arrival
            print(self, " took a spot at the table. Waited ", pretty_time(wait))
            self.table.add_player(self)
            with self.table.dealer_request(self) as dealer_request, self.table.boxman.request() as boxman_request:
                yield dealer_request and boxman_request
                yield env.timeout(seconds(45))
            env.process(self.play(env))
        else:
            spot_request.cancel()
            self.t_departure = env.now
            wait = self.t_departure - self.t_arrival
            print(self, " reneged after ", pretty_time(wait))

    def depart(self, env):
        self.t_departure = env.now
        played = self.t_departure - self.t_seated
        yield self.table.spots.release(self.spot)
        self.table.remove_player(self)
        print(self, " departed at ", pretty_time(env.now), " after playing ", pretty_time(played))

    def shoot(self, env):
        pass

    def play(self, env):
        yield env.timeout(self.play_time)
        env.process(self.depart(env))

    def place_bet(self, env):
        with self.table.request_dealer(self) as dealer_request:
            yield dealer_request
            yield env.timeout(10)
