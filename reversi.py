
# reversi game
# some simplifications: ignore diagonals, only turn those opposite pieces that
#  are in the row/column that is being played (ignore secondary capture)
# we encode white as 1 and black as -1

import numpy as np

S = 8

def all_legal(own):
  # return coordinates of empty that are legal move for 1 or -1
  # can be horizontal or vertical
  # has own at either end and opposite in the middle
  coord = []
  opp = 1 if own == -1 else -1
  for a in range(S):
    for s in range(S - 3):
      for e in range(s + 3, S):
        row = board[a, s:e]
        col = board[s:e, a]
        if legal(row, own, opp):
          start = (a, s)
          end = (a, e - 1)
          coord.append((start, end))
        if legal(col, own, opp):
          start = (s, a)
          end = (e - 1, a)
          coord.append((start, end))
  return coord

def all(x, cond):
  s = sum([1 if i == cond else 0 for i in x])
  return s == len(x)

def legal(x, own, opp):
  # can be 0,[opp],own or own,[opp],0
  assert len(x) > 2
  if ((x[0] == 0 and x[-1] == own) or (x[0] == own and x[-1] == 0)) and all(x[1:-1], opp):
    return True
  return False

def turn_opposite(own, xy):
  # turn opponents into own
  opp = 1 if own == -1 else -1
  if xy[0][0] == xy[1][0]: # if x dim same: row
    for y in range(xy[0][1], xy[1][1] + 1):
      board[xy[0][0], y] = own
  else:
    for x in range(xy[0][0], xy[0][1] + 1):
      board[x, xy[1][1]] = own

def random_move(legal):
  n = np.random.randint(len(legal))
  return legal[n]

def max_move(legal):
  # make the move with most turns
  legal = sorted(legal, key=lambda x: max(x[1][0] - x[0][0], x[1][1] - x[0][1]),
    reverse=True)
  return legal[0]

def new_board():
  # 0 are empty, 1 is white, -1 is black
  board = np.zeros((S, S))
  board[3, 3] = 1
  board[4, 4] = 1
  board[3, 4] = -1
  board[4, 3] = -1
  return board

def winner():
  w = np.sum(board == 1)
  b = np.sum(board == -1)
  print(w, b)
  if w > b:
    return 1
  elif b > w:
    return -1
  else:
    return 0


# test it
board = new_board()
print(board)
print(winner())

print(all([1, 1], 1))

print(legal([0, 1, 1, -1], -1, 1)) # is legal
print(legal([0, -1, 1, -1], -1, 1)) # not legal

print(all_legal(1))
print(all_legal(-1))

leg = all_legal(1)

turn_opposite(1, leg[0])
print(max_move(leg))

print(board)

print(all_legal(-1))

# now play a game, 50 rounds
# white makes max move and black makes random move

board = new_board()

own = 1

for i in range(50):
  leg = all_legal(own)
  if len(leg) > 0:
    if own == 1:
      move = max_move(leg)
    else:
      move = random_move(leg)
    turn_opposite(own, move)
  else:
    print(own, 'cannot move')
  own = 1 if own == -1 else -1
  
print(board)
print(winner())  
