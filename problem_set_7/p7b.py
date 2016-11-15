import random

def coin_flip():
    """
    returns true if heads
    :return:
    """
    return random.random() > 0.5

def three_heads():
    ## calculate prob of 3 heads in sequence
    num_trials = 10000000
    success = 0

    for n in range(0,num_trials):
        result = []

        for f in range(0,3):
            # print coin_flip()
            result.append(coin_flip())

        if False not in result:
            success += 1

    print "simulation result: " + str(success / float(num_trials))
    print "theoretical result is (0.5)^3: " + str(0.5**3)

def head_tail_head():
    ## calculate prob of 3 heads in sequence
    num_trials = 10000000
    success = 0

    for n in range(0,num_trials):
        result = []

        for f in range(0,3):
            # print coin_flip()
            result.append(coin_flip())

        if result == [True, False, True]:
            success += 1

    print "simulation result: " + str(success / float(num_trials))
    print "theoretical result is (0.5)^3: " + str(0.5**3)

def one_tail():
    ## calculate prob of 3 heads in sequence
    num_trials = 10000000
    success = 0

    for n in range(0,num_trials):
        result = []

        for f in range(0,3):
            # print coin_flip()
            result.append(coin_flip())

        if result.count(True) == 2:
            success += 1

    print "simulation result: " + str(success / float(num_trials))
    print "theoretical result is (0.5)^3 * 3: " + str((0.5**3)*3)

def head_gt_tail():
    ## calculate prob of 3 heads in sequence
    num_trials = 1000
    success = 0

    for n in range(0,num_trials):
        result = []

        for f in range(0,3):
            # print coin_flip()
            result.append(coin_flip())

        if result.count(True) >= result.count(False):
            success += 1
            # print result

    print "simulation result: " + str(success / float(num_trials))
    print "theoretical result: P(seq with 2 heads) + P(seq with 3 heads)"
    print "theoretical result is (0.5)^3 * 3 + (0.5)^3: " + str((0.5**3)*3 + (0.5**3))

def dice_roll():
    return random.randint(1,6)

def yahtzee(num_dice):

    num_trials = 1000000
    success = 0

    for n in range(0, num_trials):
        result = []

        for d in range(0, num_dice):
            result.append(dice_roll())

        if result.count(result[0]) == len(result):
            success += 1

    return success / float(num_trials)

if __name__ == '__main__':

    # here we selcet what to run
    # three_heads()
    # head_tail_head()
    # one_tail()
    # head_gt_tail()

    ## yahtzee
    print "theoretical probability = 6 * (1/6)^5"
    print "theoretical probability = " + str(6 * (1/float(6))**5)

    result = yahtzee(5)
    print "monte carlo probability: " + str(result)



