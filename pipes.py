#!/usr/bin/env python

import argparse
import re
import sys

INPUT_LINE_RE = re.compile(r'(?P<coin>\w+):(?P<x>\d+),(?P<y>\d+)')

def convert2locdict(game_board):
    locdict = {}
    for k, v in game_board.items():
        for new_k in v:
            locdict[new_k] = k
    return locdict

def display(no_of_rows, game_board):
    locdict = convert2locdict(game_board)
    rage_of_rc = range(no_of_rows)
    def draw_line():
        sys.stdout.write('+')
        for column in rage_of_rc: sys.stdout.write('--+')
        print
    draw_line()
    for row in rage_of_rc:
        sys.stdout.write('|')
        for column in rage_of_rc:
            sys.stdout.write(' %s|' % locdict.get((row, column),' '))
        print
        draw_line()

def read_input(file_name):
    game_board = {}
    with open(file_name,'r') as in_file:
        no_of_rows = int(in_file.readline())
        for line in in_file:
            mat = INPUT_LINE_RE.match(line)
            if mat:
                values = mat.groupdict()
                game_board.setdefault(values['coin'], []).append(
                    (int(values['x']),int(values['y'])))
            else:
                assert False, "error in input line %s" % line
        return no_of_rows, game_board

def main():
    parser = argparse.ArgumentParser(description='Solve pipes problem.')
    parser.add_argument('file_ids', metavar='N', type=int, nargs='+',
                        help='file ids, this will be used as input<id>.txt')
    arg = parser.parse_args()
    for file_id in arg.file_ids:
        no_of_rows, game_board = read_input("input/input%s.txt" % file_id)
        display(no_of_rows, game_board)
        # output = solve(input)
        # display(output)

if __name__ == '__main__':
    main()
