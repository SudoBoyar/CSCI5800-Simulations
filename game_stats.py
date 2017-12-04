class GameStats(object):

    def __init__(self, table):
        self.table = table

        self.crap_out = 0
        self.pass_line_hit = 0
        self.points_set = 0
        self.points_hit = 0
        self.seven_out = 0

        self.table.env.process(self.watch())

    def watch(self):
        while self.table.next_roll_event is not None:
            yield self.table.next_roll_event

            roll, point = self.table.roll_event.value

            if roll is None:
                continue

            if point is not None:
                if roll == point:
                    self.points_hit += 1
                elif roll == 7:
                    self.seven_out += 1
            else:
                if roll in [2, 3, 12]:
                    self.crap_out += 1
                elif roll in [7, 11]:
                    self.pass_line_hit += 1
                else:
                    self.points_set += 1

    def data(self):
        return {
            'Crap Out': self.crap_out,
            'Pass Line Hit': self.pass_line_hit,
            'Points Set': self.points_set,
            'Points Hit': self.points_hit,
            'Seven Out': self.seven_out,
        }
