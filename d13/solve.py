# part 1
fname = 'input.txt'
inp = open(fname).read().split('\n\n')

from collections import namedtuple
# Datastructure to hold the increments for a button
XY = namedtuple('XY', ['x', 'y'])
Game = namedtuple('Game', ['a', 'b', 'goal'])
games = []
for ip in inp:
    lines = ip.split('\n')
    get_button = lambda button: list(map(lambda x: int(x.split('+')[1]), lines[button].split(':')[1].strip().split(',')))
    # a = list(map(lambda x: int(x.split('+')[1]), lines[0].split(':')[1].strip().split(',')))
    a = XY(*get_button(0))
    b = XY(*get_button(1))
    # print(a, b)

    goal = XY(*list(map(lambda x: int(x.split('=')[1]), lines[2].split(':')[1].strip().split(','))))
    game = Game(a, b, goal)
    print(game)
    games.append(game)


def play(game):
    '''
    Play the game.
    Looks like we're trying to solve a system of equations.

    For example:
    MAT = [
        94, 34
        22, 67
    ]
    x = [
        A,
        B
    ]
    b = [
        8400,
        5400
    ]
    Find all possible x solutions to the system of equations and then
    return the solution with the smallest cost,
    cost = [
        3, 1
    ]

    MAT @ x = b

    A_moves = (ax_delta * num_a, ay_delta * num_a)
    B_moves = (bx_delta * num_b, by_delta * num_b)
    prize = A_moves + B_moves
    prize_x = ax_delta * num_a + bx_delta * num_b
    prize_y = ay_delta * num_a + by_delta * num_b

    [                   [                               [
        prize_x,    =       ax_delta, bx_delta,     @       num_a,
        prize_y,            ay_delta, by_delta              num_b
    ]                   ]                               ]

    There's the system of equations.
    I believe that there will always be 1 or 100 solutions.
    num_a = prize_x / (bx_delta * num_b)
    
    [               [                   [
        s0,    =       a0, b0,     @       x0,
        s1,            a1, b1              x1
    ]               ]                   ]
    s0 = a0*x0 + b0*x1
    s1 = a1*x0 + b1*x1

    x1 = (s0 - a0 * x0) / b0
    s1 = a1 * x0 + b1 * (s0 - a0 * x0) / b0
    b0 * s1 = a1 * b0 * x0 + b1 * (s0 - a0 * x0)
    b0 * s1 = a1 * b0 * x0 + b1 * s0 - b1 * a0 * x0
    b0 * s1 - b1 * s0 = x0 * (a1 * b0 - b1 * a0)
    ^x0 = (b0 * s1 - b1 * s0) / (a1 * b0 - b1 * a0)

    ^x1 = (s1 - a1 * ^x0) / b1
    '''

    # Use closed form solution. Only handle cases where there is exactly one solution for now.
    print(f'Game: {game}')
    a, b, goal = game.a, game.b, game.goal
    neg_det = (a.y * b.x - b.y * a.x)
    assert neg_det != 0, f'determinant must not be zero, got {neg_det}'
    numer = (b.x * goal.y - b.y * goal.x)
    num_a = numer / neg_det
    if int(num_a) != num_a:
        print(f'Game is impossible')
        return 0
    num_a = int(num_a)
    num_b = (goal.y - a.y * num_a) / b.y
    if int(num_b) != num_b:
        print(f'Game is impossible')
        return 0
    num_b = int(num_b)

    print(f'Solution: A: {num_a}, B: {num_b}')
    return 3 * num_a + num_b
    
ret = 0
for game in games:
    ret += play(game)

print(ret)

# part 2:
offset = 10000000000000
ret = 0
for game in games:
    new_goal = XY(game.goal.x+offset, game.goal.y+offset)
    new_game = Game(game.a, game.b, new_goal)
    ret += play(new_game)
print(ret)