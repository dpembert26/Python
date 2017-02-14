import argparse
import operator

parse = argparse.ArgumentParser(description = "This script will give the total of the numbers put in.")
parse.add_argument("integers", type=int, metavar='N', nargs="+",
                   help="Numbers for the accumulator/subtractor")

parse.add_argument("--sum", dest="add", action="store_const",
                   const=sum, default=max, help="Add the numbers or give the max")


args = parse.parse_args()

print(args.add(args.integers))
