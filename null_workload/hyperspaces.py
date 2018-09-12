# script to create hyperspaces 

from hyperspace.space import create_hyperspace

def get_hyperspaces(parameters = None):

    f = open("spaces.txt", "w")
    hyperspace = create_hyperspace(hyperparameters)
    f.write(hyperspace)
    return hyperspace


if __name__ == '__main__':
  
    get_hyperspaces(parameters = int(sys.argv[1]))
    




