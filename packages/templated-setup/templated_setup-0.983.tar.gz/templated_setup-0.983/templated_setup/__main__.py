# During the testing of this module via another project of mine.
# I found that the module was not being imported correctly.
#
# The problem is that the os.path variable is might not be set correctly.
#
# See, when pip tries to install a package that is using our nifty `templated_setup` package,
# it will download whatever `x` package is but then during the process of parsing the `setup.py` file,
# it will try to import the `templated_setup` package.
#
# And sometimes, the `os.path` variable is not set correctly, so pip cannot find the `templated_setup` package.

# This is a simple fix for that problem.
# We will write a small __main__.py to replace the commonly used `python setup.py install` or whatever commands.



import os
import argparse
import pip
import sys



DESC = """This small helper script is used to replace the `python setup.py install` or what have you set of commands."""

parser = argparse.ArgumentParser(description=DESC)

parser.add_argument("command", choices=['install', 'uninstall', 'build'], help="The command to run.")
parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass to the command.")
args = parser.parse_args()

if not args.command in ["install", "uninstall", "build"]:
	raise ValueError("Invalid command.")



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATED_SETUP_PARENT_PATH = os.path.join(BASE_DIR, "..")
sys.path.insert(0, TEMPLATED_SETUP_PARENT_PATH)



def install(args):
	pip.main(["install"] + args)



def uninstall(args):
	pip.main(["uninstall"] + args)



def build(args):
	pip.main(["build"] + args)



if args.command == "install":
	install(args.args)
elif args.command == "uninstall":
	uninstall(args.args)
elif args.command == "build":
	build(args.args)



