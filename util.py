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
        return size, game_board

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

def convert2locdict(game_board, raise_error=True):
        locdict = {}
        for k, v in game_board.items():
            for new_k in v:
                if new_k in locdict:
                    if raise_error:
                        raise KeyError('Overlapping paths')
                    return None
                locdict[new_k] = k
        return locdict
