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
    def __init__(self, name, results_dir):
        # this task will execute Bayesian optimizations
         
        super(OptimizationTask, self).__init__()
        self.name = name
        self.copy_input_data   = []
        self.copy_input_data  += ['$SHARED/example.py']
        self.copy_input_data  += ['$SHARED/t10k-images-idx3-ubyte.gz']
        self.copy_input_data  += ['$SHARED/t10k-labels-idx1-ubyte.gz']
        self.copy_input_data  += ['$SHARED/train-images-idx3-ubyte.gz']
        self.copy_input_data  += ['$SHARED/train-labels-idx1-ubyte.gz']
        self.pre_exec    =   []
        self.pre_exec   += ['export PATH="/home/dakka/miniconda3/bin:$PATH"']
        self.pre_exec   += ['export LD_LIBRARY_PATH="/home/dakka/miniconda3/lib:$LD_LIBRARY_PATH"']
        self.pre_exec   += ['module load mpi/gcc_openmpi']
        self.pre_exec   += ['source activate ve_hyperspace']
        # self.pre_exec   += ['module load mpi/intel_mpi'] 
        self.executable  = ['python']
        self.arguments   = ['example.py', '--results_dir', results_dir]
        self.cpu_reqs    = {'processes': 4, 'thread_type': None, 'threads_per_process': 28, 'process_type': 'MPI'}


if __name__ == '__main__':

    # arguments for AppManager

    hparams = 2

    p = HyperSpacePipeline(name = 'hyperspace_pipeline')

    # Stage 1: single task that spawns n_optimizations using mpirun

    s1 = OptimizationStage(name = 'optimizations')

    t1 = OptimizationTask(name = 'analysis_1', results_dir = '/pylon5/mc3bggp/dakka/hyperspace_data/results_1/skopt/space4') 

    s1.add_tasks(t1)
    p.add_stages(s1)

    s2 = OptimizationStage(name = 'optimizations')

    t2 = OptimizationTask(name = 'analysis_2', results_dir = '/pylon5/mc3bggp/dakka/hyperspace_data/results_2/skopt/space4' )

    s2.add_tasks(t2)
    p.add_stages(s2)
        

    s3 = OptimizationStage(name = 'optimizations')

    t3 = OptimizationTask(name = 'analysis_3', results_dir = '/pylon5/mc3bggp/dakka/hyperspace_data/results_3/skopt/space4')

    s3.add_tasks(t3)
    p.add_stages(s3)
        

    logger.info('adding stage {} with {} tasks'.format(s1.name, s1._task_count))
    logger.info('adding pipeline {} with {} stages'.format(p.name, p._stage_count))

    # Create Application Manager
    appman = AppManager(hostname=hostname, port=port)

    res_dict = {

        'resource': 'xsede.bridges',
        'project' : 'mc3bggp',
        'queue' : 'RM',
        'walltime': 90,
        'cpus': (2**hparams)*28,
        'access_schema': 'gsissh'
    }


    # Assign resource manager to the Application Manager
    appman.resource_desc = res_dict
    appman.shared_data   = []
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/gbm/space2/optimize.py']
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/data/fashion/t10k-images-idx3-ubyte.gz']
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/data/fashion/t10k-labels-idx1-ubyte.gz']
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/data/fashion/train-images-idx3-ubyte.gz']
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/data/fashion/train-labels-idx1-ubyte.gz']
    appman.shared_data += ['%s/binaries/example.py' %cur_dir]
                    
    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.workflow = [p]

    # Run the Application Manager
    appman.run()

