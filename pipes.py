#!/usr/bin/env python

import argparse
import re
import sys

INPUT_LINE_RE = re.compile(r'(?P<coin>\w+):(?P<x>\d+),(?P<y>\d+)')

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

def get_possible_directions(locdict, size, start, end):
    possible_iters = range(-1,2)
    for r in possible_iters:
        for c in possible_iters:
            # n -> next
            n_r, n_c = start[0]+r, start[1]+c
            if abs(r+c)==1 and (size > n_r >= 0) and (size > n_c >= 0):
                n_coin = locdict.get((n_r, n_c), None)
                if (not n_coin):
                    yield n_r, n_c, False
                elif n_r == end[0] and n_c == end[1]:
                    yield n_r, n_c, True

class GameBoard(object):

    def __init__(self, size, game_board):
        self.size = size
        self.game_board = game_board

    def convert2locdict(self):
        self.locdict = {}
        for k, v in self.game_board.items():
            for new_k in v:
                self.locdict[new_k] = k
        return self.locdict

    def display(self):
        if not hasattr(self, 'locdict'): self.convert2locdict()
        rage_of_rc = range(self.size)
        def draw_line():
            sys.stdout.write('+')
            for column in rage_of_rc: sys.stdout.write('--+')
            print
        draw_line()
        for row in rage_of_rc:
            sys.stdout.write('|')
            for column in rage_of_rc:
                sys.stdout.write(' %s|' % self.locdict.get(
                    (row, column),' '))
            print
            draw_line()


    def solve(self):
        self.display()
        for coin, locs in self.game_board.items():
            for dir_r,dir_c,end  in get_possible_directions(
                    self.locdict, self.size, *locs):
                print dir_r,dir_c,end
                self.locdict[(dir_r, dir_c)] = coin

def main():
    parser = argparse.ArgumentParser(description='Solve pipes problem.')
    parser.add_argument('file_ids', metavar='N', type=int, nargs='+',
                        help='file ids, this will be used as input<id>.txt')
    arg = parser.parse_args()
    for file_id in arg.file_ids:
        game_board = read_input("input/input%s.txt" % file_id)
        output = game_board.solve()
        game_board.display()
        # display(output)

if __name__ == '__main__':
    main()
