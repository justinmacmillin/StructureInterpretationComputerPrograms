"""The Game of Hog"""

from dice import four_sided_dice, six_sided_dice, make_test_dice
from ucb import main, trace, log_current_line, interact

goal = 100          # The goal of Hog is to score 100 points.
commentary = False  # Whether to display commentary for every roll.


# Taking turns

def roll_dice(num_rolls,  dice=six_sided_dice, who='Boss Hogg' ):
    """Calculate WHO's turn score after rolling DICE for NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A function of no args and returns an integer outcome.
    who:        Name of the current player, for commentary.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    turn_score = 0
    while num_rolls > 0:
        roll = dice()
        if roll == 1:
            turn_score = 1
        else:
            if turn_score == 1:
                turn_score = 1
            else:
                turn_score = turn_score + roll
        if commentary:
            announce(roll, who)
        num_rolls = num_rolls - 1
    return turn_score

def take_turn(num_rolls, opponent_score, dice=six_sided_dice, who='Boss Hogg'):
    """Simulate a turn in which WHO chooses to roll NUM_ROLLS, perhaps 0.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args and returns an integer outcome.
    who:             Name of the current player, for commentary.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    if commentary:
        print(who, 'is going to roll', num_rolls, 'dice')
    #Account for Free Bacon rule
    if num_rolls == 0:
        return opponent_score // 10 + 1
    else:
        return roll_dice(num_rolls, dice, who)
    
def take_turn_test():
    """Test the roll_dice and take_turn functions using test dice."""
    print('-- Testing roll_dice with deterministic test dice --')
    dice = make_test_dice(4, 6, 1)
    assert roll_dice(2, dice) == 10, 'First two rolls total 10'

    dice = make_test_dice(4, 6, 1)
    assert roll_dice(3, dice) == 11, 'Third roll is a 1'

    dice = make_test_dice(1, 2, 3)
    assert roll_dice(3, dice) == 6, 'First roll is a 1'

    print('-- Testing take_turn --')
    dice = make_test_dice(4, 6, 1)
    assert take_turn(2, 0, dice) == 10, 'First two rolls total 10'

    dice = make_test_dice(4, 6, 1)
    assert take_turn(3, 20, dice) == 11, 'Third roll is a 1'

    assert take_turn(0, 34) == 4, 'Opponent score 10s digit is 3'
    assert take_turn(0, 71) == 8, 'Opponent score 10s digit is 7'
    assert take_turn(0,  7) == 1, 'Opponont score 10s digit is 0'

    '*** You may add more tests here if you wish ***'

    print('Tests for roll_dice and take_turn passed.')


# Commentator

def announce(outcome, who):
    """Print a description of WHO rolling OUTCOME."""
    print(who, 'rolled a', outcome)
    print(draw_number(outcome))

def draw_number(n, dot='*'):
    """Return a text representation of rolling the number N.
    If a number has multiple possible representations (such as 2 and 3), any
    valid representation is acceptable.

    >>> print(draw_number(5))
     -------
    | *   * |
    |   *   |
    | *   * |
     -------

    >>> print(draw_number(6, '$'))
     -------
    | $   $ |
    | $   $ |
    | $   $ |
     -------
    """
    if n == 1:
        die = draw_dice(True, False, False, False, dot)
    elif n ==2:
        die = draw_dice(False, False, True, False, dot)
    elif n ==3:
        die = draw_dice(True, False, True, False, dot)
    elif n ==4:
        die = draw_dice(False, True, True, False, dot)
    elif n == 5:
        die = draw_dice(True, True, True, False, dot)
    else:
        die = draw_dice(False, True, True, True, dot)
    return die

def draw_dice(c, f, b, s, dot):
    """Return an ASCII art representation of a die roll.

    c, f, b, & s are boolean arguments. This function returns a multi-line
    string of the following form, where the letters in the diagram are either
    filled if the corresponding argument is true, or empty if it is false.

     -------
    | b   f |
    | s c s |
    | f   b |
     -------

    The sides with 2 and 3 dots have 2 possible depictions due to rotation.
    Either representation is acceptable.

    This function uses Python syntax not yet covered in the course.

    c, f, b, s -- booleans; whether to place dots in corresponding positions.
    dot        -- A length-one string to use for a dot.
    """
    assert len(dot) == 1, 'Dot must be a single symbol'
    border = ' -------'
    def draw(b):
        return dot if b else ' '
    c, f, b, s = map(draw, [c, f, b, s])
    top = ' '.join(['|', b, ' ', f, '|'])
    middle = ' '.join(['|', s, c, s, '|'])
    bottom = ' '.join(['|', f, ' ', b, '|'])
    return '\n'.join([border, top, middle, bottom, border])


# Game simulator

def num_allowed_dice(score, opponent_score):
    """Return the maximum number of dice allowed this turn. The maximum
    number of dice allowed is 10 unless the sum of SCORE and
    OPPONENT_SCORE has a 7 as its ones digit.

    >>> num_allowed_dice(1, 0)
    10
    >>> num_allowed_dice(5, 7)
    10
    >>> num_allowed_dice(7, 10)
    1
    >>> num_allowed_dice(3, 24)
    1
    """
    if (score + opponent_score) % 10 == 7:
        return 1
    else:
        return 10

def select_dice(score, opponent_score):
    """Select 6-sided dice unless the sum of scores is a multiple of 7.

    >>> select_dice(4, 24) == four_sided_dice
    True
    >>> select_dice(16, 64) == six_sided_dice
    True
    """
    #Hog Wild
    if (score + opponent_score) % 7 == 0:
        return four_sided_dice
    else:
        return six_sided_dice

def other(who):
    """Return the other player, for players numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return (who + 1) % 2

def name(who):
    """Return the name of player WHO, for player numbered 0 or 1."""
    if who == 0:
        return 'Player 0'
    elif who == 1:
        return 'Player 1'
    else:
        return 'An unknown player'

def play(strategy0, strategy1):
    """Simulate a game and return 0 if the first player wins and 1 otherwise.

    A strategy function takes two scores for the current and opposing players.
    It returns the number of dice that the current player will roll this turn.

    If a strategy returns more than the maximum allowed dice for a turn, then
    the maximum allowed is rolled instead.

    strategy0:  The strategy function for player 0, who plays first.
    strategy1:  The strategy function for player 1, who plays second.
    """
    who = 0 # Which player is about to take a turn, 0 (first) or 1 (second)
    player0_score, player1_score = 0, 0 #initiate players' scores
    while player0_score < goal and player1_score < goal:
        if who == 0:
            intended_rolls = strategy0(player0_score, player1_score)
            if intended_rolls > num_allowed_dice(player0_score, player1_score):
                rolls = num_allowed_dice(player0_score, player1_score)
            else:
                rolls = intended_rolls
            #interact()
            turn_score = take_turn(rolls, player1_score, select_dice(player0_score, player1_score), name(who))
            player0_score = turn_score + player0_score
        else:
            if strategy1(player1_score, player0_score) > num_allowed_dice(player1_score, player0_score):
                rolls = num_allowed_dice(player1_score, player0_score)
            else:
                rolls = strategy1(player1_score, player0_score)
            #interact()
            turn_score = take_turn(rolls, player0_score, select_dice(player0_score, player1_score), name(who))
            player1_score = turn_score + player1_score
        who = other(who)
    if player0_score >= goal:
        return 0
    else:
        return 1


# Basic Strategy

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two game scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice to roll.

    If a strategy returns more than the maximum allowed dice for a turn, then
    the maximum allowed is rolled instead.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


# Experiments (Phase 2)

def make_average(fn, num_samples=100000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> avg_dice = make_average(dice)
    >>> avg_dice()
    3.75
    >>> avg_score = make_average(roll_dice)
    >>> avg_score(2, dice, False)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    def averager(*args):
        total = 0
        n = num_samples
        while n > 0:
            total = total + fn(*args)
            n -= 1
        return total/num_samples
    return averager


def compare_strategies(strategy, baseline=always_roll(5)):
    """Return the average win rate (out of 1) of STRATEGY against BASELINE."""
    as_first = 1 - make_average(play)(strategy, baseline)
    as_second = make_average(play)(baseline, strategy)
    return (as_first + as_second) / 2  # Average the two results

def eval_strategy_range(make_strategy, lower_bound, upper_bound):
    """Return the best integer argument value for MAKE_STRATEGY to use against
    the always-roll-5 baseline, between LOWER_BOUND and UPPER_BOUND (inclusive).

    make_strategy -- A one-argument function that returns a strategy.
    lower_bound -- lower bound of the evaluation range.
    upper_bound -- upper bound of the evaluation range.
    """
    best_value, best_win_rate = 0, 0
    value = lower_bound
    while value <= upper_bound:
        strategy = make_strategy(value)
        win_rate = compare_strategies(strategy)
        print('Win rate against the baseline using', value, 'value:', win_rate)
        if win_rate > best_win_rate:
            best_win_rate, best_value = win_rate, value
        value += 1
    return best_value

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:
        result = eval_strategy_range(always_roll, 1, 10)
        print('Best always_roll strategy:', result)

    if False: # Change to True when ready to test make_comeback_strategy
        result = eval_strategy_range(make_final_strategy, 1, 10)
        print('Best comeback strategy:', result)
    
    if True: # Change to True when ready to test make_comeback_strategy
        result = eval_strategy_range(make_comeback_strategy, 5, 15)
        print('Best comeback strategy:', result)

    if True: # Change to True when ready to test make_mean_strategy
        result = eval_strategy_range(make_mean_strategy, 1, 10)
        print('Best mean strategy:', result)

    if False: # Change to True when ready to test make_lead_strategy
        result = eval_strategy_range(make_lead_strategy, 1, 20)
        print('Best lead strategy:', result)

    if False: # Change to True when ready to test make_lead_strategy
        result = eval_strategy_range(make_delta_strategy, 15, 25)
        print('Best delta strategy:', result)

    "*** You may add additional experiments here if you wish ***"


# Strategies

def make_delta_strategy(deltaScore, num_rolls=5):
    """Return Strategy for when close to winning"""
    def delta_strategy(score, opponent_score):
        if goal - score <= deltaScore:
            return num_rolls - 1
        else:
            return num_rolls
    return delta_strategy

def make_lead_strategy(margin, num_rolls=5):
    """Return strategy for when you're leading"""
    def lead_strategy(score, opponent_score):
        if score - opponent_score >= margin:
            return num_rolls - 1
        else:
            return num_rolls
    return lead_strategy

def make_comeback_strategy(margin, num_rolls=5):
    """Return a strategy that rolls one extra time when losing by MARGIN."""
    def comeback_strategy(score, opponent_score):
        if opponent_score - score >= margin:
            return num_rolls + 1
        else:
            return num_rolls
    return comeback_strategy

def make_mean_strategy(min_points, num_rolls=5):
    """Return a strategy that attempts to give the opponent problems."""
    def mean_strategy(score, opponent_score):
        roll_0 = score + opponent_score + take_turn(0,opponent_score)
        if take_turn(0, opponent_score) >= min_points and roll_0 % 7 == 0 or roll_0 % 10 == 7:
            return 0
        else:
            return num_rolls
    return mean_strategy

def make_final_strategy(margin):
    """return our final strategy for lots of tests"""
    def final_strategy(score, opponent_score):
        """Write a brief description of your final strategy.

        *** YOUR DESCRIPTION HERE ***
        """
        roll_0 = score + opponent_score + take_turn(0,opponent_score) #sum if you roll 0 dice
        deltaScore = goal - score
        margin = opponent_score - score
        num_rolls = 6
        if deltaScore <= 15:
            if deltaScore <= take_turn(0, opponent_score) or roll_0 % 7 == 0 or roll_0 % 10 == 7:
                return 0
            else:
                return 3
        elif margin >= 12:
            if take_turn(0, opponent_score) >= 8 and roll_0 % 7 == 0 or roll_0 % 10 == 7:
                return 0
            else:
                return num_rolls + margin
        elif margin < -15:
            if take_turn(0, opponent_score) >= 8 and roll_0 % 7 == 0 or roll_0 % 10 == 7:
                return 0
            else:
                return num_rolls - margin
        return num_rolls
    return final_strategy

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    Strategy goes from most explicit to most general. Used optimal values of mean_strategy, comeback_strategy, and always_roll as base cases. 
    Then implemented specific end game cases that either help to keep a lead, roll more when about to lose, or take advantage or the Free Bacon Rule.
    """
    roll_0 = score + opponent_score + take_turn(0,opponent_score) #sum if you roll 0 dice
    deltaScore = goal - score
    margin = opponent_score - score
    num_rolls = 6
    if take_turn(0, opponent_score) >= 4 and roll_0 % 7 == 0 or roll_0 % 10 ==7:
        return 0
    elif deltaScore <= take_turn(0, opponent_score):
        return 0
    elif num_allowed_dice(score, opponent_score) == 1:
        return 0
    elif select_dice(score, opponent_score) == four_sided_dice and deltaScore <= 15: 
        return 0
    elif select_dice(score, opponent_score) == four_sided_dice and deltaScore >= 15: 
        return num_rolls - 2
    elif goal - opponent_score <= 10 and deltaScore >= 30:
        return num_rolls + 2
    elif goal - opponent_score <= 30 and deltaScore >= 60:
            return num_rolls + 4
    elif margin >= 8:
        return num_rolls + 1
    else:
        return num_rolls


def final_strategy_test():
    """Compares final strategy to the baseline strategy."""
    print('-- Testing final_strategy --')
    print('Win rate:', compare_strategies(final_strategy))



# Interaction.  You don't need to read this section of the program.

def interactive_strategy(score, opponent_score):
    """Prints total game scores and returns an interactive tactic.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    print('Current score:', score, 'to', opponent_score)
    while True:
        response = input('How many dice will you roll? ')
        try:
            result = int(response)
        except ValueError:
            print('Please enter a positive number')
            continue
        if result < 0:
            print('Please enter a non-negative number')
        else:
            return result

def play_interactively():
    """Play one interactive game."""
    global commentary
    commentary = True
    print("Shall we play a game?")
    winner = play(interactive_strategy, always_roll(5))
    if winner == 0:
        print("You win!")
    else:
        print("The computer won.")

def play_basic():
    """Play one game in which two basic strategies compete."""
    global commentary
    commentary = True
    winner = play(always_roll(5), always_roll(6))
    if winner == 0:
        print("Player 0, who always wants to roll 5, won.")
    else:
        print("Player 1, who always wants to roll 6, won.")

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--take_turn_test', '-t', action='store_true')
    parser.add_argument('--play_interactively', '-p', action='store_true')
    parser.add_argument('--play_basic', '-b', action='store_true')
    parser.add_argument('--run_experiments', '-r', action='store_true')
    parser.add_argument('--final_strategy_test', '-f', action='store_true')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if execute:
            globals()[name]()
