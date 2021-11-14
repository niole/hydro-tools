#!/usr/bin/env python3

import argparse
from typing import Iterable

import numpy as np

def verify_x(inputs: Iterable[int], x: Iterable[int]) -> Iterable[int]:
    inputs_matrix = np.array(inputs)
    same_nutrients_per_row_matrix = inputs_matrix.transpose()

    x_vector = np.array(x)
    return np.dot(same_nutrients_per_row_matrix, x_vector)

def solve_for_multiples(inputs: Iterable[Iterable[int]], target: Iterable[int]) -> Iterable[int]:
    inputs_matrix = np.array(inputs)
    same_nutrients_per_row_matrix = inputs_matrix.transpose()
    target_array = np.array(target)
    return np.linalg.solve(same_nutrients_per_row_matrix, target_array)

def parse_npk(npk: str) -> Iterable[int]:
    return [int(n) for n in npk.split('-')]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the ratios and amount of fertilizers to add to water')
    parser.add_argument('--inputs', required=True, type=str, nargs='+',
        help='The n-p-k ratios of the input solutions, inputted in the following format: <n1>-<p1>-<k1> <n2>-<p2...')
    parser.add_argument('--target', default=None, type=int, nargs='+',
                    help='The target n-p-k ratio to achieve with the input solutions.')
    parser.add_argument('--x', type=float, default=None, nargs='+', required=False, help='input solutions multiplers. The inputs will be multiplied with this when it is supplied and the first number of the returned vector is the multiplier for the first solution and so on')
    args = parser.parse_args()

    inputs = [parse_npk(s) for s in args.inputs]

    if args.x is None:
        if args.target is None:
            raise Exception('Provide --target when calculating x for --inputs')

        print(solve_for_multiples(inputs, args.target))
    else:
        print(verify_x(inputs, args.x))

