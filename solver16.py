#!/bin/python
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#
from Queue import PriorityQueue
from random import randrange, sample
import heapq
import sys
import string

# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)]
    return ( state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print '%3d %3d %3d %3d' % (row[j:(j+4)])


# return a list of possible successor states
def successors(state):
    return [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ]

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)

# calculate heuristics
def cal_h(state):
        # define goal state
        goal_list = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)

        #calculate heuristics h_m based on manhattan distance including the edge conditions
        h_m = [[0 for x in range(4)] for y in range(4)]
        for x1,x2 in zip(state,goal_list):
             a1 = (x1-1)%4;
             b1 = (x1-1)/4;
             a2 = (x2-1)%4;
             b2 = (x2-1)/4;
             # checking for edge condition, if the tile's position is exactly opposite add 1, else 1 + number of horizontal or vertical moves
             if (b1 == 0 and b2 == 3 and a1 == a2) or (b1 == 3 and b2 == 0 and a1 == a2):
                  h_m[b2][a2] = 1
             elif (b1 == 0 and b2 == 3 and a1 != a2) or (b1 == 3 and b2 == 0 and a1 != a2):
                  h_m[b2][a2] = 1 + abs(a1-a2)
             elif (a1 == 0 and a2 == 3 and b1 == b2) or (a1 == 3 and a2 == 0 and b1 == b2):
                  h_m[b2][a2] = 1
             elif (a1 == 0 and a2 == 3 and b1 != b2) or (a1 == 3 and a2 == 0 and b1 != b2):
                  h_m[b2][a2] = 1 + abs(b1-b2)
             else:
                   h_m[b2][a2] = abs(a1-a2)+abs(b1-b2)

        # h is heuristics for number of moves, here we are calculating the number of moves based on the number of tiles whose position have changed. For example if two moves were made - U1
        # L1 then 3+3 tiles will move 1 position and 1 tile will move 2 position. We are also giving priority to movement of either only columns or rows.
        h = 0
        for i in range(0,4):
                if (len(set(h_m[:][i])) == 1 and h_m[:][i] != [0,0,0,0]):
                        h = h + 1
                elif (len(set(h_m[:][i])) == 2 and h_m[:][i].count(0) < 3):
                        h = h + 2
                elif (len(set(h_m[:][i])) == 3 and h_m[:][i].count(0) < 2):
                        h = h + 3
                elif (len(set(h_m[:][i])) == 4 and h_m[:][i].count(0) < 1):
                        h = h + 4
                if (len(set(h_m[i][:])) == 1 and h_m[i][:] != [0,0,0,0]):
                        h = h + 1
                elif (len(set(h_m[i][:])) == 2 and h_m[i][:].count(0) < 3):
                        h = h + 2
                elif (len(set(h_m[i][:])) == 3 and h_m[i][:].count(0) < 2):
                        h = h + 3
                elif (len(set(h_m[i][:])) == 4 and h_m[i][:].count(0) < 1):
                        h = h + 4

        # this will calculate the number of misplaced tiles
        h_t = 0
        (succ)= state
        a = sorted(succ)
        b = list(succ)
        for i in range(len(a)):
             if a[i] != b[i]:
                h_t=h_t+1

        # h_m_sum is the sum of all the mahattan distances
        h_m_sum = sum( [ sum(h_m[:][i]) for i in range(0,4) ])

        # it seems that, manhattan distance as heuristics is working the best among the above three heuristics and also, when we sum up all or two combinations of heuristics
        #return h_m_sum + h_t
        return h_m_sum



# The solver! - using BFS right now
def solve(initial_board):
    fringe = []
    heapq.heappush(fringe,(0,(initial_board, "")))
    cost_so_far = {}
    cost_so_far[initial_board] = 0
    while len(fringe) > 0:
        (p,(state, route_so_far)) = heapq.heappop(fringe)
        for (succ, move) in successors( state):
            if is_goal(succ):
                return( route_so_far + " " + move)
            cost = cost_so_far[state] + 1
            if succ not in cost_so_far or cost < cost_so_far[succ]:
                cost_so_far[succ] = cost
                f= cost + cal_h(succ)
                data = (succ, route_so_far + " " + move )
                heapq.heappush(fringe,(f,data))
    return False



# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

if len(start_state) != 16:
    print "Error: couldn't parse start state file"

#print "Start state: "
#print_board(tuple(start_state))

#print "Solving..."
route = solve(tuple(start_state))

#print "Solution found in " + str(len(route)/3) + " moves:" + "\n" + route
print route
