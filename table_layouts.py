from bet import *
from odds import *


def bets(table):
    return [
        ###
        # Come out bets - no point set
        ###
        ComeOutBet(table, 'Pass Line', Odds(251, 244), Payout(1, 1), [7, 11], [2, 3, 12]),
        ComeOutBet(table, "Don't Pass Line", Odds(976, 949), Payout(1, 1), [2, 3, 12], [7, 11]),

        ###
        # Point set
        ###
        PointBet(table, 'Place 4', Odds(2, 1), Payout(9, 5), [4], [7]),
        PointBet(table, 'Place 5', Odds(3, 2), Payout(7, 5), [5], [7]),
        PointBet(table, 'Place 6', Odds(6, 5), Payout(7, 6), [6], [7]),
        PointBet(table, 'Place 8', Odds(6, 5), Payout(7, 6), [8], [7]),
        PointBet(table, 'Place 9', Odds(3, 2), Payout(7, 5), [9], [7]),
        PointBet(table, 'Place 10', Odds(2, 1), Payout(9, 5), [10], [7]),

        FieldBet(table),

        ###
        #  Prop bets - Always on
        ###
        # Hard Way Prop Bets
        PropBet(table, 'Hard 4', Odds(8, 1), Payout(7, 1), [7, [2, 2]], [[1, 3]]),
        PropBet(table, 'Hard 6', Odds(10, 1), Payout(9, 1), [7, [3, 3]], [[1, 5], [2, 4]]),
        PropBet(table, 'Hard 8', Odds(10, 1), Payout(9, 1), [7, [4, 4]], [[3, 5], [2, 6]]),
        PropBet(table, 'Hard 10', Odds(8, 1), Payout(7, 1), [7, [5, 5]], [[4, 6]]),

        # Single Roll Prop Bets
        SingleRoll(table, 'Snake Eyes', Odds(35, 1), Payout(30, 1), [2]),
        SingleRoll(table, 'Three', Odds(17, 1), Payout(15, 1), [3]),
        SingleRoll(table, 'Yo', Odds(17, 1), Payout(15, 1), [11]),
        SingleRoll(table, 'Midnight', Odds(35, 1), Payout(30, 1), [12]),
        SingleRoll(table, 'Any Craps', Odds(8, 1), Payout(7, 1), [2, 3, 12]),
        SingleRoll(table, 'Any Seven', Odds(6, 1), Payout(4, 1), [7]),

        # All, Tall, and Small - point only prop bets
        AllBet(table),
        TallBet(table),
        SmallBet(table),
    ]
