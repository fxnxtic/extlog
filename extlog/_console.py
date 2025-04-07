import os
import sys
import argparse
import traceback


parser = argparse.ArgumentParser()
parser.add_argument('name', type=str)
args = parser.parse_args()


if sys.platform == "win32":
    from colorama import just_fix_windows_console
    just_fix_windows_console()

if args.name:
    os.system("title " + str(args.name))


try:
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        print(line, end="")

    sys.exit(0)
except:
    sys.stdout.write(traceback.format_exc())
