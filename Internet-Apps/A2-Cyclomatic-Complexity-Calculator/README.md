# CS4400-Internet-Applications-Repo-Complexity

Calculates Cyclomatic Complexity of the python files contained in JCass45's (me) Chat Server repository, distributing the work across multiple worker nodes.

## How to use

* Pull the project down to a remote machine for the master to run on.
* Activate the virtual environment using `. venv/bin/activate`
* Build the worker docker image using `docker build -t worker.py .`
* Deploy the worker docker image to a docker repository so that it can be pulled down onto a remote machine.
* Pull the worker docker image down to a separate remote machine.
* Start the master using `python master.py` (make sure the virtual env is activated). The master downloads a list of commit SHA's and starts a Flask server from which the workers can steal work
* On the workers remote machine, use `. run_workers x` to startup x containers for the worker docker image. 
* You should see on the master side all of the workers beginning to steal work with a `'New node joined'` console message

## Results

The master appends the time taken for x workers to complete the task to the results.txt file. After finished running the master with varying combinations of workers, the results.txt can be graphed by running `python plot_results.py` which will output a pyplot graph of Workers vs Time.
![A sample graph](https://github.com/JCass45/CS4400-Internet-Applications-Repo-Complexity/blob/master/workers-vs-time.png "A graph of workers ranging from 5 to 20. The task was repeated twice for each quantity of workers and mean averaged")
