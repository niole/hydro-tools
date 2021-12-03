#!/usr/bin/env python3

import argparse
import math

GREEN_TOTAL_TSPS_ONE = 43.0
YELLOW_TOTAL_TSPS_ONE = 26.0

QUARTER_CS_DIV = 2.0 # this may confuse me in the future, bc these divisors refer to the previous measurement size
EIGHTH_CS_DIV = 2.0
TBSPS_DIV = 3.0

def check_work_test(measures, tsps_target) -> (int, int):
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

    return (found_tsps, tsps_target)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the ratio of micro, bloom, green to add to the green or yellow bucket')
    parser.add_argument('--debug',action='store_true', default=None, required=False, help='debug ec calculation')
    parser.add_argument('--green',action='store_true', default=None, required=False, help='green bucket')
    parser.add_argument('--yellow',action='store_true', default=None, required=False, help='yellow bucket')
    parser.add_argument('--ec', default=None, required=True, type=float)
    args = parser.parse_args()


    if args.green:
        if args.debug:
            print("should be equal", check_work_test(simplify(green_tsps(args.ec)), green_tsps(args.ec)))
        print(format_labels(simplify(green_tsps(args.ec))))
    elif args.yellow:
        if args.debug:
            print("should be equal", check_work_test(simplify(yellow_tsps(args.ec)), yellow_tsps(args.ec)))
        print(format_labels(simplify(yellow_tsps(args.ec))))
    else:
        raise Exception("Provide --green or --yellow")

