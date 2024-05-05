#/usr/bin/env python
import os
import yaml
import subprocess
import argparse

parser = argparse.ArgumentParser(
                    prog='taguchi',
                    description='performs taguchi based experiments',
                    epilog='see https://github.com/jcranney/taguchi for more info.')

parser.add_argument('-v', '--verbose',
            action='count', default=0)  # on/off flag
args = parser.parse_args()
verbose = args.verbose

with open("./taguchi.yaml","r") as f:
    a : dict = yaml.full_load(f)

#print(a)

command = a.pop("command")

params = list(a.keys())
n_params = len(params)
n_states = len(a[params[0]])

orthogonal_arrays = {
    (3,2) : 
       [[0,0,0],
        [0,1,1],
        [1,0,1],
        [1,1,0]]
}

try:
    array = orthogonal_arrays[(n_params,n_states)]
except KeyError as e:
    raise NotImplementedError(f"{n_params:d} params with {n_states:d} states not supported.")

results = []
for experiment in array:
    for param,state in zip(params,experiment):
        os.environ[param] = str(a[param][state])
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if verbose:
        print(out)
        print(err)
    out = out.decode().split("\n")
    result = None
    for o in out:
        try:
            result = float(o)
        except ValueError:
            pass
    if result is None:
        raise ValueError("No number found in output of command")
    
    results.append(result)

for j,param in enumerate(params):
    print(f"{param:12s}")
    for i,state in enumerate(a[param]):
        res = 0.0
        n_experiment = 0
        for k,experiment in enumerate(array):
            if experiment[j]==i:
                res += results[k]
                n_experiment += 1
        print(f"{state:12} : {res/n_experiment:12f}")