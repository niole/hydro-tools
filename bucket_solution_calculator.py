#!/usr/bin/env python3

import argparse
import math
from typing import Iterable

import solution_ratio_calculator as ratio_calculator

M_B_G_SOLUTIONS = [[5,0,1], [0,5,4], [2,1,6]]

GREEN_TOTAL_TSPS_ONE = 43.0
YELLOW_TOTAL_TSPS_ONE = 26.0

QUARTER_CS_DIV = 2.0 # this may confuse me in the future, bc these divisors refer to the previous measurement size
EIGHTH_CS_DIV = 2.0
TBSPS_DIV = 3.0

def check_work_test(measures, tsps_target) -> bool:
    found_tsps = 0.0
    for i in range(len(measures)):
        if i == 0:
            found_tsps += measures[i][0]
        elif i == 1:
            found_tsps += measures[i][0]*TBSPS_DIV
        elif i == 2:
            found_tsps += measures[i][0]*TBSPS_DIV*EIGHTH_CS_DIV
        elif i == 3:
            found_tsps += measures[i][0]*TBSPS_DIV*EIGHTH_CS_DIV*QUARTER_CS_DIV

    return found_tsps == tsps_target

def format_labels(measures) -> str:
    labels = [f"{m} {label}" for (m, label) in measures if m > 0]
    return ", ".join(labels)

def simplify(base_tsps: float):
    tbsps_base = math.floor(base_tsps/TBSPS_DIV) # this is the max # of tbsps, but what we ultimately keep is subject to how many eigths
    eigth_cs_base = math.floor(tbsps_base/EIGHTH_CS_DIV)

    tsps = base_tsps%TBSPS_DIV # after converting out tbsps, the remainig tiny bit is in tsps
    tbsps = tbsps_base%EIGHTH_CS_DIV
    eigth_cs = eigth_cs_base%QUARTER_CS_DIV
    quarter_cs = math.floor(eigth_cs_base/QUARTER_CS_DIV)

    return [(tsps, "tsps"), (tbsps, "tbsps"), (eigth_cs, "eigth_cs"), (quarter_cs, "quarter_cs")]

def green_tsps(ec: float) -> float:
    return GREEN_TOTAL_TSPS_ONE*ec

def yellow_tsps(ec: float) -> float:
    return YELLOW_TOTAL_TSPS_ONE*ec

def create_instructions(total_tsps: float, npk: Iterable[float], debug: bool) -> str:
    solution_proportions = ratio_calculator.solve_for_multiples(M_B_G_SOLUTIONS, args.npk)
    normalized_proportions =  [sol/sum(solution_proportions) for sol in solution_proportions]
    solutions_tsps = [total_tsps*proportion for proportion in normalized_proportions]
    instructions = [format_labels(simplify(ts)) for ts in solutions_tsps]

    if debug:
        debug_inputs(
            total_tsps=total_tsps,
            npk_target=npk,
            proportions=normalized_proportions,
            solutions_tsps=solutions_tsps
        )

    return f"micro: {instructions[0]},\nbloom: {instructions[1]}\ngreen: {instructions[2]}"

def check_npk_from_solution_proportions(proportions: Iterable[float], npk_target: Iterable[float]) -> bool:
    # sums up npk from solution proportions, makes sure that it is a ratio of npk_target
    n = 0.0
    p = 0.0
    k = 0.0
    for (sol, proportion) in zip(M_B_G_SOLUTIONS, proportions):
        n += sol[0]*proportion
        p += sol[1]*proportion
        k += sol[2]*proportion

    # if ratio of total of each macro nutrient to the target is the same for all nutrients, we are correct
    ratios = [s/t for (s, t) in zip([n, p, k], npk_target)]
    return all([ratios[0] == r for r in ratios])

def do_test(msg: str, actual, expected):
    if actual != expected:
        raise Exception(f"{msg}: {actual} should be {expected}")

def debug_inputs(total_tsps: float, npk_target: Iterable[float], proportions: Iterable[float], solutions_tsps: Iterable[float]):
    try:
        do_test("solutions tsps should be in the right proportion with total requested tsps", solutions_tsps, [total_tsps*p for p in proportions])
        do_test("solutions tsps should add up to total_tsps", sum(solutions_tsps), total_tsps)
        do_test("npk from the combination of solutions should be the same as requested", check_npk_from_solution_proportions(proportions, npk_target), True)
        do_test("simplify should return the right amount of liquid, only simplified", check_work_test(simplify(total_tsps), total_tsps), True)
        print("\nNothing wrong here.\n")
    except Exception as e:
        print(f"\n{e}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the ratio of micro, bloom, green to add to the green or yellow bucket')
    parser.add_argument('--debug',action='store_true', required=False, help='debug ec calculation')
    parser.add_argument('--green',action='store_true', required=False, help='green bucket')
    parser.add_argument('--yellow',action='store_true', required=False, help='yellow bucket')
    parser.add_argument('--ec', required=True, type=float)
    parser.add_argument('--npk', required=True, type=int, nargs='+',
                    help='The target n-p-k ratio to achieve with the input solutions.')
    args = parser.parse_args()

    if args.green:
        total_tsps = green_tsps(args.ec)
        out = create_instructions(total_tsps, args.npk, args.debug)
        print(out)
    elif args.yellow:
        total_tsps = yellow_tsps(args.ec)
        out = create_instructions(total_tsps, args.npk, args.debug)
        print(out)
    else:
        raise Exception("Provide --green or --yellow")

