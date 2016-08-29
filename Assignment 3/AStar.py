"""
Josh Johnson
This is an A* algorithm that uses heuristics to run a modified depth-first search.
CSE 415
"""
import sys
import importlib
from heapq import *
from operator import itemgetter
import operator


if sys.argv == [''] or len(sys.argv) < 2:
    import BasicEightPuzzle as Problem
else:
    Problem = importlib.import_module(sys.argv[1])
    userHeuristic = getattr(Problem, sys.argv[2])
    puzzle = importlib.import_module(sys.argv[3])


print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}


def runAStar():
    initial_state = puzzle.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(Problem.DESCRIBE_STATE(initial_state))
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    IterativeAStar(initial_state)
    print(str(COUNT) + " states examined.")


def IterativeAStar(initial_state):
    global COUNT, BACKLINKS

    OPEN = [initial_state]
    CLOSED = []
    BACKLINKS[Problem.HASHCODE(initial_state)] = -1
    heuristic = {Problem.HASHCODE(initial_state): 0}

    while OPEN != []:
        S = OPEN[0]
        del OPEN[0]
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            backtrace(S)
            return

        COUNT += 1
        if (COUNT % 32) == 0:
            print(".", end="")
            if (COUNT % 128) == 0:
                print("COUNT = " + str(COUNT))
                print("len(OPEN)=" + str(len(OPEN)))
                print("len(CLOSED)=" + str(len(CLOSED)))
        L = []
        for op in Problem.OPERATORS:
            # Optionally uncomment the following when debugging
            # a new problem formulation.
            # print("Trying operator: "+op.name)
            if op.precond(S):
                new_state = op.state_transf(S)
                if not occurs_in(new_state, CLOSED):
                    L.append(new_state)
                    BACKLINKS[Problem.HASHCODE(new_state)] = S
                    # add this for the heuristic
                    heuristic[Problem.HASHCODE(new_state)] = heuristic[Problem.HASHCODE(S)] + 1
                    # Uncomment for debugging:
                    # print(Problem.DESCRIBE_STATE(new_state))

        for s2 in L:
            for i in range(len(OPEN)):
                if Problem.DEEP_EQUALS(s2, OPEN[i]):
                    del OPEN[i];
                    break

        OPEN = L + OPEN
        OPEN = sorted(OPEN, key = lambda x: tempCompare(x, heuristic))


def tempCompare(x, heuristic):
    return heuristic[Problem.HASHCODE(x)] + userHeuristic(x)


def backtrace(S):
    global BACKLINKS

    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[Problem.HASHCODE(S)]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(Problem.DESCRIBE_STATE(s))
    return path


def occurs_in(s1, lst):
    for s2 in lst:
        if Problem.DEEP_EQUALS(s1, s2): return True
    return False

if __name__ == '__main__':
    runAStar()
