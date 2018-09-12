# script to create hyperspaces 

from hyperspace.space import create_hyperspace
import pickle

def get_hyperspaces(parameters = None):

    hyperspaces = create_hyperspace(hyperparameters)
    with open('spaces.txt', 'wb') as fp:
        pickle.dump(hyperspaces, fp)
    return hyperspaces


if __name__ == '__main__':
  
    get_hyperspaces(parameters = int(sys.argv[1]))
    




