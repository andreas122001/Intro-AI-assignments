import multiagent.pacman as pac
import sys

args = pac.readCommand(sys.argv[1:])
pac.runGames(**args)
