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
        # this task will execute Bayesian optimizations using GBM 
         
        super(OptimizationTask, self).__init__()
        self.name = name
        self.copy_input_data  = ['$SHARED/optimize.py']
        self.copy_input_data  += ['$SHARED/t10k-images-idx3-ubyte.gz']
        self.copy_input_data  += ['$SHARED/t10k-labels-idx1-ubyte.gz']
        self.copy_input_data  += ['$SHARED/train-images-idx3-ubyte.gz']
        self.copy_input_data  += ['$SHARED/train-labels-idx1-ubyte.gz']
        
        self.pre_exec    =   []
        self.pre_exec   += ['export PATH="/home/dakka/miniconda3/bin:$PATH"']
        self.pre_exec   += ['export LD_LIBRARY_PATH="/home/dakka/miniconda3/lib:$LD_LIBRARY_PATH"']
        self.pre_exec   += ['module load mpi/gcc_openmpi']
        self.pre_exec   += ['source activate ve_hyperspace']

        self.executable  = ['python']
        self.arguments   = ['optimize.py', '--data_path', '/pylon5/mc3bggp/dakka/hyperspace_data/constellation/constellation/data/fashion', 
                            '--results_dir', '/pylon5/mc3bggp/dakka/hyperspace_data/results_shared_fs']
        self.cpu_reqs    = {'processes': 16, 'thread_type': None, 'threads_per_process': 28, 'process_type': 'MPI'}
        

        # self.pre_exec    =   []
        # self.pre_exec   += ['export PATH="/home/dakka/miniconda3/bin:$PATH"']
        # self.pre_exec   += ['export LD_LIBRARY_PATH="/home/dakka/miniconda3/lib:$LD_LIBRARY_PATH"']
        # self.pre_exec   += ['module load mpi/gcc_openmpi']
        # self.pre_exec   += ['source activate ve_hyperspace']
        # self.pre_exec   += ['mkdir fashion']
        # self.pre_exec   += ['mv *.gz fashion']
        
        # self.copy_input_data += ['$SHARED/t10k-labels-idx1-ubyte.gz']
        # self.copy_input_data += ['$SHARED/train-images-idx3-ubyte.gz']
        # self.copy_input_data += ['$SHARED/train-labels-idx1-ubyte.gz']
        # self.copy_input_data += ['$SHARED/t10k-images-idx3-ubyte.gz']
        # self.executable  = ['python']
        # self.arguments   = ['optimize.py', '--data_path', '/fashion',
        #                     '--results_dir', '/home/dakka/hyperspace/constellation/constellation/gbm/space4/results_shared_data']
        # self.cpu_reqs    = {'processes': 4, 'thread_type': None, 'threads_per_process': 28, 'process_type': 'MPI'}
        # self.download_output_data = ['/home/dakka/hyperspace/constellation/constellation/gbm/space4/results_shared_data/*']

if __name__ == '__main__':

    # arguments for AppManager

    hparams = 4

    p = HyperSpacePipeline(name = 'hyperspace_pipeline')

    # Stage 1: single task that spawns n_optimizations using mpirun

    s = OptimizationStage(name = 'optimizations') 

     for cnt in range(3):
        t = OptimizationTask(name = 'optimizations using gbm')
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
        'walltime': 80*3,
        'cpus': (2**hparams)*28,
        'access_schema': 'gsissh'
    }


    # Assign resource manager to the Application Manager
    appman.resource_desc = res_dict
    appman.shared_data  = ['/home/jdakka/hyperspace/constellation/constellation/gbm/space4/optimize.py']
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/data/fashion/t10k-images-idx3-ubyte.gz']
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/data/fashion/t10k-labels-idx1-ubyte.gz']
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/data/fashion/train-images-idx3-ubyte.gz']
    appman.shared_data += ['/home/jdakka/hyperspace/constellation/constellation/data/fashion/train-labels-idx1-ubyte.gz']
    
    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.workflow = [p]

    # Run the Application Manager
    appman.run()

