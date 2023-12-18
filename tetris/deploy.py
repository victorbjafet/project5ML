from game import Game
import sys
import pickle


def main():
    # game = Game(sys.argv[1]) #if you want to run from the command line with an arguement (this was formerly main.py)
    game = Game("genetic_victor", pickle.load(open("agents/ai2289-990.pkl", 'rb')))
    game.run_no_visual()
    # game.run()

    


if __name__ == "__main__":
    main()
