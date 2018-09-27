# script to create hyperspaces 

from hyperspace.space import create_hyperspace
import pickle



def get_hyperspaces(parameters = None, sampler=None, n_samples=None):

'''

     * `sampler` [str, default=None]
        Random sampling scheme for optimizer's initial runs.
        Options:
        - "lhs": latin hypercube sampling
    * `n_samples` [int, default=None]
        Number of random samples to be drawn from the `sampler`.
        - Required if you would like to use `sampler`.
        - Must be <= the number of elements in the smallest hyperparameter bound's set.

'''

    hyperspaces = create_hyperspace(hyperparameters)
    
    with open('/home/dakka/spaces.txt', 'wb') as fp: # add the location an argument save known place
        pickle.dump(hyperspaces, fp)

    if sampler and not n_samples:
            raise ValueError(f'Sampler requires n_samples > 0. Got {n_samples}')
    elif sampler and n_samples:
        # if samples is false, its value is returned, otherwise n_samples is evaluated and 
        # the resulting value is returned
        hyperbounds = create_hyperbounds(hyperparameters)
    return hyperspaces






