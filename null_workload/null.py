from radical.entk import Pipeline, Stage, Task, AppManager
import os
import traceback
import sys
# from hyperspace.space import create_hyperspace

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


class HyperSpaceTask(Task):
    def __init__(self, name, parameter):

        self.name = name
        self.executable = ['/bin/sleep']
        self.arguments = ['100']
        # self.arguments = ['-c', '24', '-t', '600']
        # self.arguments = ['.sh file']
        self.parameters = parameter
        self.cpu_reqs =  {
        
                        'processes': 24,
                        'process_type': None/MPI,
                        'threads_per_process': 1,
                        'thread_type': None/OpenMP
                    }


if __name__ == '__main__':

    # arguments for AppManager
    total_cores = sys.argv[1] # 2**H*24 
    duration = sys.argv[2] 


    # define the global search space bounds for each search dimension

    hparams = [(0,7), (10,17)] 

    # generate all combinations of search subspaces (hyperspaces)

    # spaces = SpaceTask.CreateSpaces(parameters = hparams)

    pipelines = set()
    p = Pipeline()
    s = Stage() # 1 stage of bag-of-tasks (2**H tasks)

    for i in (len(hparams)**2): # for each hyperspace
    
        t = HyperSpaceTask(name = 'optimization_{}'.format(i), parameter = i) 
        # run Bayesian optimization for N-iterations in parallel
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
        'port' : 33048,
        'hostname': 'localhost'}


   