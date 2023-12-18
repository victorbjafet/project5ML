import numpy as np
from copy import copy, deepcopy
import random
from genetic_helpers import *


class Genetic_AI_Victor:
    def __init__(self, genotype=None, num_features=9, mutate=False,  mutation_rate=.2):

        if(genotype is None):
            # makes a genotype randomly valued from -1 to 1 for EACH FEATURE (array of 9 values from -1 to 1)
            self.genotype = np.array([random.uniform(-1, 1) for _ in range(num_features)])
        else:
            if(mutate == False):
                self.genotype = genotype
            else:
                # mutate the weights
                mutation = np.array([np.random.normal(1, mutation_rate) for i in range(num_features)])
                self.genotype = genotype * mutation


    def valuate(self, board): # mostly taken from genetic.py as well since it handles all the features i need just like genetic_helper

        peaks = get_peaks(board)
        highest_peak = np.max(peaks)
        holes = get_holes(peaks, board)
        wells = get_wells(peaks)

        rating_funcs = {
            'agg_height': np.sum(peaks),
            'n_holes': np.sum(holes),
            'bumpiness': get_bumpiness(peaks),
            'num_pits': np.count_nonzero(np.count_nonzero(board, axis=0) == 0),
            'max_wells': np.max(wells),
            'n_cols_with_holes': np.count_nonzero(np.array(holes) > 0),
            'row_transitions': get_row_transition(board, highest_peak),
            'col_transitions': get_col_transition(board, peaks),
            'cleared': np.count_nonzero(np.mean(board, axis=1))
        }


        ratings = np.array([*rating_funcs.values()], dtype=float)
        
        aggregate_rating = np.dot(ratings, self.genotype) #applies the actual weights to each of the features

        return aggregate_rating


    def get_best_move(self, board, piece): #taken directly from genetic.py since it's the same for every ai

        best_x = -1000 
        max_value = -1000 #best value given from a certain move (starts at -1000 so ofc it can only go up)
        best_piece = None
        for i in range(4): #goes through each possible rotation
            piece = piece.get_next_rotation()
            for x in range(board.width): #goes through each possible x value for the piece at this rotation
                try: #gets the height of the piece when dropped (done in a try except since this framework is kind of broken in places)
                    y = board.drop_height(piece, x)
                except:
                    continue

                board_copy = deepcopy(board.board)
                for pos in piece.body: #drops the piece on a copy of the board so that that board can be evaluated
                    board_copy[y + pos[1]][x + pos[0]] = True

                np_board = bool_to_np(board_copy) #changes the board to be np formatted to work with the valuate function
                c = self.valuate(np_board) #gets the score of the board (this does all the actual magic of using features and their weights to determine the score of a move)

                if c > max_value: #if this move happens to be better than any move before it, update all the variables to be this move
                    max_value = c #updates new best move score
                    best_x = x #updates new best x value
                    best_piece = piece #updates new best rotation
        return best_x, best_piece #returns the best x and best rotation after all possible moves were checked
