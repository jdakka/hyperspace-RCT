# hyperspace
Distributed Bayesian Hyperparameter Optimization using RCT 


### Installation on `xsede.bridges` via miniconda3


```
* wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
* bash Miniconda3-latest-Linux-x86_64.sh
* conda create --name <VE name> python=3.6
* source activate /home/dakka/.conda/envs/<VE name> or source activate <VE name>
* conda install scikit-learn
* git clone git@github.com:yngtodd/hyperspace.git
* cd hyperspace; python setup.py install 
```
* check to see if all libraries are installed (`pip freeze`) 
