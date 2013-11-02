#!/usr/bin/env python

import argparse
from itertools import product
from util import read_input, display, convert2locdict, convert2gameboard

possible_iters = (-1,0,1)
possible_moves = [ (r, c) for r in possible_iters \
                   for c in possible_iters if abs(r+c)==1 ]

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

def remove_obviously_wrong(paths, size_sq):
    print {k:len(v) for k,v in paths.items()}
    print "size_sq:", size_sq
    min_path_lens = {k:min([len(path) for path in v]) for k,v in paths.items()}

    max_path_lens = {coin:(size_sq-sum([v for k,v in min_path_lens.items()\
                                        if k != coin])
                       ) for coin in paths.keys()}
    new_paths = {coin:[path for path in paths[coin] if len(path)<=max_len] \
                 for coin,max_len in max_path_lens.items()}
    print {k:len(v) for k,v in new_paths.items()}
    return new_paths

def solve(size, start_game_board):
    start_locdict = convert2locdict(start_game_board)
    size_sq = size ** 2
    display(start_locdict, size)
    paths = {}
    for coin, locs in start_game_board.items():
        paths[coin] = []
        for path in get_paths(coin, start_locdict.copy(),
                              size, [locs[0]], locs[-1]):
            paths[coin].append(path)
    paths = remove_obviously_wrong(paths, size_sq)
    combo_len=len(paths.keys())
    locdict = None
    count=0
    for combo in product(*paths.values()):
        total_length = sum([len(path) for path in combo])
        count+=1
        if count%100000==0:
            print "checked %d combos, tl: %d" % (count, total_length)
        if total_length == size_sq:
            possible_gb = convert2gameboard(start_locdict, combo)

            locdict = convert2locdict(possible_gb,
                                      raise_error=False)
            if locdict:
                print "possible combo", combo
                break
        else:
            continue
    print "total %d combos checked" % count
    if locdict:
        display(locdict, size)
    else:
        print "can't find solution."

def main():
    parser = argparse.ArgumentParser(description='Solve pipes problem.')
    parser.add_argument('file_ids', metavar='N', type=int, nargs='+',
                        help='file ids, this will be used as input<id>.txt')
    arg = parser.parse_args()
    for file_id in arg.file_ids:
        solve(*read_input("input/input%s.txt" % file_id))

if __name__ == '__main__':
    main()
