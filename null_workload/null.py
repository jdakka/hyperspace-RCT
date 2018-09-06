from radical.entk import Pipeline, Stage, Task, AppManager
import os
import traceback
import sys

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


# creates a class of type Task
class GenHyperTask(Task):
    def __init__(self, name):

        self.name = name
        self.pre_exec = ['export PATH=/u/sciteam/dakka/stress-ng/stress-ng-0.09.34:$PATH']
        self.executable = ['stress-ng']
        self.arguments = ['-c', '1', '-t', '600']
        
        self.cpu_reqs =  {

                        'processes': 1,
                        'process_type': None/MPI,
                        'threads_per_process': 1,
                        'thread_type': None/OpenMP
                    } 
        self.post_exec = [] 

class HyperSpaceTask(Task, parameters):
    def __init__(self, name, parameters):

        self.name = name
        self.executable = ['stress-ng']
        self.arguments = ['-c', '1', '-t', '600']
        self.parameters = parameters 

        self.cpu_reqs =  {
        
                        'processes': 1,
                        'process_type': None/MPI,
                        'threads_per_process': 1,
                        'thread_type': None/OpenMP
                    }



if __name__ == '__main__':

    # arguments for stress-ng 
    cores_per_task = sys.argv[1] 
    duration = sys.argv[2] 

    # Set up parameters

    # For each model:
        # generate hyperparameters 
        # for each hyperparameter: 
            # assign hyperspaces 
            # run hyperspaces 


    pipelines = set()
    p = Pipeline()

    steps = ['create-parameters', 'hyperspaces']
    hparams = [(0,7), (10,17)] # two sets of hyperparameters (lower, upper)

    s1 = Stage() # create hyperparameters step 
    t = GenHyperTask(name = 'create-parameters') # returns hyperspaces 
    s1.add_tasks(t)

    s2 = Stage() # optimizations (2**H tasks) 

    for i in (len(hparams)**2):
        t = HyperSpaceTask(name = 'optimization_{}'.format(i), parameter) 
        t.arguments = []
        s2.add_tasks(t)
    p.add_stage(s2)


    # for step in workflow:
    #     s, t = Stage(), NullTask(name=step, cores=cores_per_pipeline)
    #     t.arguments = ['replica_{}/lambda_{}/{}.conf'.format(replica, ld, step), '&>', 'replica_{}/lambda_{}/{}.log'.format(replica, ld, step)]
    #     s.add_tasks(t)
    #     p.add_stage(s)

    pipelines.add(p)


    # Resource and AppManager

    
    amgr.workflow = pipelines
    amgr.shared_data = []


    amgr = AppManager()
    amgr.resource_desc = {
        'resource': 'xsede.bridges',
        'walltime': 10,
        'cpus': 1,
        'rmq_cleanup': true,
        'autoterminate': true,
        'port' = 33048,
        'hostname': 'localhost'}


   