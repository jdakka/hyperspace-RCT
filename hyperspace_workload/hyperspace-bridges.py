from radical.entk import Pipeline, Stage, Task, AppManager
import os
import traceback
import sys
import pickle  
from glob import glob
import radical.utils as ru
import shutil



# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'

cur_dir = os.path.dirname(os.path.abspath(__file__))
hostname = os.environ.get('RMQ_HOSTNAME','localhost')
port = int(os.environ.get('RMQ_PORT',5672))

logger = ru.Logger(__name__, level='DEBUG')

class HyperSpacePipeline(Pipeline):
    def __init__(self, name):
        super(HyperSpacePipeline, self).__init__()
        self.name = name 


class OptimizationStage(Stage):
    def __init__(self, name):
        super(OptimizationStage, self).__init__()
        self.name = name    

class OptimizationTask(Task):
    def __init__(self, name):
        # this task will execute Bayesian optimizations
         
        super(OptimizationTask, self).__init__()
        self.name = name
        self.copy_input_data = ['$SHARED/example.py']
        self.pre_exec    =   []
        self.pre_exec   += ['export PATH="/home/dakka/miniconda3/bin:$PATH"']
        self.pre_exec   += ['export LD_LIBRARY_PATH="/home/dakka/miniconda3/lib:$LD_LIBRARY_PATH"']
        self.pre_exec   += ['source activate ve_hyperspace']
        self.pre_exec   += ['module load mpi/intel_mpi'] 
        self.executable  = ['python']
        self.arguments   = ['example.py', '--results_dir', 'results/skopt/space4']
        self.cpu_reqs    = {'processes': 4, 'thread_type': None, 'threads_per_process': 28, 'process_type': 'MPI'}


if __name__ == '__main__':

    # arguments for AppManager

    hparams = 2

    p = HyperSpacePipeline(name = 'hyperspace_pipeline')

    # Stage 1: single task that spawns n_optimizations using mpirun

    s = OptimizationStage(name = 'optimizations') 

    t = OptimizationTask(name = 'optimizations using example.py')

    s.add_tasks(t)
    p.add_stages(s)
        

    logger.info('adding stage {} with {} tasks'.format(s.name, s._task_count))
    logger.info('adding pipeline {} with {} stages'.format(p.name, p._stage_count))

    # Create Application Manager
    appman = AppManager(hostname=hostname, port=port)

    res_dict = {

        'resource': 'xsede.bridges',
        'project' : 'mc3bggp',
        'queue' : 'RM',
        'walltime': 10,
        'cpus': (2**hparams)*28,
        'access_schema': 'gsissh'
    }


    # Assign resource manager to the Application Manager
    appman.resource_desc = res_dict
    appman.shared_data = ['%s/binaries/example.py' %cur_dir]
                    
    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.workflow = [p]

    # Run the Application Manager
    appman.run()

