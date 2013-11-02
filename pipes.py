#!/usr/bin/env python

import argparse
import re
import sys
from itertools import product

INPUT_LINE_RE = re.compile(r'(?P<coin>\w+):(?P<x>\d+),(?P<y>\d+)')

possible_iters = (-1,0,1)
possible_moves = [ (r, c) for r in possible_iters \
                   for c in possible_iters if abs(r+c)==1 ]

def read_input(file_name):
    game_board = {}
    with open(file_name,'r') as in_file:
        size = int(in_file.readline())
        for line in in_file:
            mat = INPUT_LINE_RE.match(line)
            if mat:
                values = mat.groupdict()
                game_board.setdefault(values['coin'], []).append(
                    (int(values['x']),int(values['y'])))
            else:
                assert False, "error in input line %s" % line
        return GameBoard(size, game_board)

def display(locdict, size):
    rage_of_rc = range(size)
    def draw_line():
        sys.stdout.write('+')
        for column in rage_of_rc: sys.stdout.write('--+')
        print
    draw_line()
    for row in rage_of_rc:
        sys.stdout.write('|')
        for column in rage_of_rc:
            sys.stdout.write(' %s|' % locdict.get(
                (row, column),' '))
        print
        draw_line()

def get_directions(locdict, size, start, end):
    for r, c in possible_moves:
        # n -> next
        n_r, n_c = start[0]+r, start[1]+c
        if (size > n_r >= 0) and (size > n_c >= 0):
            n_coin = locdict.get((n_r, n_c), None)
            if (not n_coin):
                yield n_r, n_c, False
            elif n_r == end[0] and n_c == end[1]:
                yield n_r, n_c, True


def get_paths(coin, locdict, size, path, end):
    for dir_r,dir_c,did_end  in get_directions(
            locdict, size, path[-1], end):
        path.append((dir_r, dir_c))
        if did_end:
            # display(locdict, size)
            yield path[:]
        else:
            new_locdict = locdict.copy()
            new_locdict[(dir_r, dir_c)] = coin
            for new_path in get_paths(coin, new_locdict, size, path, end):
                yield new_path
        path.pop()

class GameBoard(object):

    def __init__(self, size, game_board):
        self.size = size
        self.size_sq = size ** 2
        self.start_game_board = game_board

    def convert2locdict(self, game_board=None, raise_error=True):
        locdict = {}
        if not game_board:
            game_board = self.start_game_board
        for k, v in game_board.items():
            for new_k in v:
                if new_k in locdict:
                    if raise_error:
                        raise KeyError('Overlapping paths')
                    return None
                locdict[new_k] = k
        return locdict

    def convert2gameboard(self, paths):
        return {self.start_locdict[path[0]]:path for path in paths}

    def solve(self):
        self.start_locdict = self.convert2locdict()
        display(self.start_locdict, self.size)
        self.paths = {}
        for coin, locs in self.start_game_board.items():
            self.paths[coin] = []
            for path in get_paths(coin, self.start_locdict.copy(),
                                   self.size, [locs[0]], locs[-1]):
                # print path
                self.paths[coin].append(path)
        # print self.paths
        locdict = None
        for combo in product(*self.paths.values()):
            total_length = 0
            for path in combo:
                total_length+=len(path)
                if total_length > self.size_sq:
                    break
            if total_length == self.size_sq:
                possible_gb = self.convert2gameboard(combo)

                locdict = self.convert2locdict(possible_gb,
                                               raise_error=False)
                if locdict:
                    print "possible combo", combo
                    break
        if locdict:
            display(locdict, self.size)
        else:
            print "can't find solution."

def main():
    parser = argparse.ArgumentParser(description='Solve pipes problem.')
    parser.add_argument('file_ids', metavar='N', type=int, nargs='+',
                        help='file ids, this will be used as input<id>.txt')
    arg = parser.parse_args()
    for file_id in arg.file_ids:
        game_board = read_input("input/input%s.txt" % file_id)
        output = game_board.solve()
        # display(output)

if __name__ == '__main__':
    main()
