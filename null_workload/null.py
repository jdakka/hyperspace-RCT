from radical.entk import Pipeline, Stage, Task, AppManager
import os
import traceback
import sys
from hyperspace.space import create_hyperspace

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


# creates a class of type Task
class SpaceTask():
    
    def CreateSpaces(self, parameters): 

        self.hparams = parameters
        hyperspaces = create_hyperspace(hyperparameters)

    return hyperspaces 
    


class HyperSpaceTask(Task):
    def __init__(self, name, parameter):

        self.name = name
        self.executable = ['stress-ng']
        self.arguments = ['-c', '24', '-t', '600']
        self.parameters = parameter
        self.cpu_reqs =  {
        
                        'processes': 24,
                        'process_type': None/MPI,
                        'threads_per_process': 1,
                        'thread_type': None/OpenMP
                    }



if __name__ == '__main__':

    # arguments for AppManager
    total_cores = sys.argv[1] 
    duration = sys.argv[2] 


    # arguments for hyperdrive

    # * objective function
    # * model 

    # Set up parameters

    # assign lower and upper bounds of hyperparameters 
    # for each model: 
        # generate hyperparameters
        # for each hyperparameter: 
            # assign hyperspace 
            # run hyperspace  


    # input is hyperparameters's upper and lower bounds
    # compute hyperparameters for input to optimizations

    # For each model
        # for each hyperparameter:
            # run hyperspaces 

    # two sets of hyperparameters (lower, upper) boundary 

    params = [(0,7), (10,17)] 
    spaces = SpaceTask.CreateSpaces(parameters = params)

    pipelines = set()
    p = Pipeline()

    s = Stage() # optimizations (2**H tasks) 

    models = ['GP']

    # create a dictionary of model: hyperparameter boundary tuple 

    for x in len(models):
        
        # define model parameters, hyperparameters, objective function
        for i in (len(hparams)**2):

            # just fix the parameter for each, create a dictionary 
            t = HyperSpaceTask(name = 'optimization_{}'.format(i), parameter = i) 
            s.add_tasks(t)

    p.add_stage(s)
    pipelines.add(p)


    # Resource and AppManager

    
    amgr.workflow = pipelines
    amgr.shared_data = []


    amgr = AppManager()
    amgr.resource_desc = {
        'resource': 'xsede.bridges',
        'walltime': duration,
        'cpus': total_cores,
        'rmq_cleanup': true,
        'autoterminate': true,
        'port' = 33048,
        'hostname': 'localhost'}


   