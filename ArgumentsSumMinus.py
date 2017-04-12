import argparse
import operator

parse = argparse.ArgumentParser(description="This script will give the sum or the difference between two numbers.")
parse.add_argument("x", type=int, help="First number.")
parse.add_argument("y", type=int, help="Second number.")
parse.add_argument("--sum",action="count", default=0)
parse.add_argument("--minus", action="count", default=0)
args = parse.parse_args()
answer1 = args.x + args.y
answer2 = args.x - args.y

if args.sum:
    print("{} plus {} is equals to {}".format(args.x, args.y, answer1))
elif args.minus:
    print("{} minus {} is equals to {}".format(args.x, args.y, answer2))
else:
    print("Please put in either --sum or --minus before the numbers x and y")