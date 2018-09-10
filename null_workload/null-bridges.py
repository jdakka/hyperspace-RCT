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
        self.pre_exec = ['export PATH=/home/jdakka/stress-ng-0.09.39:$PATH']
        self.executable = ['stress-ng'] 
        self.arguments = ['-c', '24', '-t', '600']
      	self.cpu_reqs = {'processes': 1, 'thread_type': None, 'threads_per_process': 24, 'process_type': None}


if __name__ == '__main__':

    # arguments for AppManager
    # total_cores = int(sys.argv[1])*24 # 2**H*24 
    duration = int(sys.argv[1]) 


    # define the global search space bounds for each search dimension

    hparams = [(0,7), (10,17), (10,17), (10,17), (10,17), (10,17), (10,17), (10,17)] 
    
    # generate all combinations of search subspaces (hyperspaces)

    # spaces = SpaceTask.CreateSpaces(parameters = hparams)

    pipelines = set()
    p = Pipeline()
    s = Stage() # 1 stage of bag-of-tasks (2**H tasks)
   

    for i, param in enumerate((len(hparams)**2)): # for each hyperspace
    
        
        # run Bayesian optimization for N-iterations in parallel
        t = HyperSpaceTask(name = 'optimization_{}'.format(i), parameter = param)
	    s.add_tasks(t)

    p.add_stages(s)
    pipelines.add(p)

    # Resource and AppManager
    amgr = AppManager(hostname = 'two.radical-project.org', port = 33048)
    amgr.workflow = pipelines
    amgr.shared_data = []
   
    amgr.resource_desc = {
        'resource': 'xsede.bridges',
        'project' : 'MCB110096P',
        'queue' : 'RMS',
        'walltime': duration,
        'cpus': (len(hparams)**2)*24,
        'access_schema': 'gsissh'}
       
    amgr.run()
