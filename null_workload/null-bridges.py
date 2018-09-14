from radical.entk import Pipeline, Stage, Task, AppManager
import os
import traceback
import sys
import pickle # change the pickle to json load and dump 
import radical.utils as ru

# convert tabs to spaces (no tabs)


# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'

logger = ru.Logger(__name__, level='DEBUG')

class HyperSpacePipeline(Pipeline):
    def __init__(self, name):
        super(HyperSpacePipeline, self).__init__()
        self.name = name 

class HyperSpaceStage(Stage):
    def __init__(self, name):
        super(HyperSpaceStage, self).__init__()
        self.name = name
        

class HyperSpaceTask(Task):
    def __init__(self, name, hyperparameters):

        # this task will generate hyperspaces
        # takes input hyperparameters that are defined by user 
        # and uses HyperSpace function create_hyperspace to generate a list of 
        # hyperspaces 

        super(HyperSpaceTask, self).__init__()
        self.name = name
        self.pre_exec = ['source activate ve_hyperspace']
        self.copy_input_data = ['$SHARED/hyperspaces.py']
        self.executable = ['python']
        self.arguments = ['hyperspaces.py', 'hyperparameters']
        self.cpu_reqs = {'processes': 1, 'thread_type': None, 'threads_per_process': 1, 'process_type': None}


class OptimizationStage(Stage):
    def __init__(self, name):
        super(OptimizationStage, self).__init__()
        self.name = name    

class OptimizationTask(Task):
    def __init__(self, name, hyperspace_index):

        # this task will execute a Bayesian optimization
        # each task takes a unique hyperspace input  
        
        super(OptimizationTask, self).__init__()
        self.name = name
        self.copy_input_data = ['/home/dakka/spaces.txt','$SHARED/hyperspaces.py']
        self.pre_exec = ['export PATH=/home/dakka/stress-ng-0.09.39:$PATH']
        self.pre_exec += ['python optimization.py {}'.format(hyperspace_index)]
        self.executable = ['stress-ng'] 
        self.arguments = ['-c', '24', '-t', '6000']
        self.cpu_reqs = {'processes': 1, 'thread_type': None, 'threads_per_process': 24, 'process_type': None}



if __name__ == '__main__':

    # arguments for AppManager

    walltime = int(sys.argv[1]) 


    # user defines the global search space bounds for each search dimension

    hparams = [(0,7), (10,17)] 

    # EnTK single pipeline of two stages 

    pipelines = set()
    p = HyperSpacePipeline(name = 'hyperspace_pipeline')

    
    # Stage 1: generate all combinations of search subspaces (hyperspaces)

    s = HyperSpaceStage(name = 'generate_hyperspaces_stage')
    t = HyperSpaceTask(name = 'generate_hyperspace_task', hyperparameters = hparams)
    s.add_tasks(t) 
    p.add_stages(s)

    logger.info('adding stage {} with {} tasks'.format(s.name, s._task_count))

    # Stage 2: bag-of-tasks for Bayesian optimizations (2**H tasks) 

    s = OptimizationStage(name = 'optimizations') 
    for i in range(len(hparams)**2): 
    
        # run Bayesian optimization in parallel
        # each optimization runs for n_iterations

        t = OptimizationTask(name = 'optimization_{}'.format(i), hyperspace_index = i)
        s.add_tasks(t)
        
    p.add_stages(s)
    pipelines.add(p)

    logger.info('adding stage {} with {} tasks'.format(s.name, s._task_count))
    logger.info('adding pipeline {} with {} stages'.format(p.name, p._stage_count))

    # Resource and AppManager
    amgr = AppManager(hostname = 'two.radical-project.org', port = 33048)
    amgr.workflow = pipelines
    amgr.shared_data = ['hyperspaces.py','optimization.py']
    amgr.resource_desc = {
        'resource': 'xsede.bridges',
        'project' : 'mc3bggp',
        'queue' : 'RM',
        'walltime': walltime,
        'cpus': len(hparams)**2*24,
        'access_schema': 'gsissh'}
       
    amgr.run()
