#! /usr/bin/env python
##
## A benchmarking (fake) step parsing params, inputs and outputs
##
## Started 22 Feb 2024
## Izaskun Mallona

import sys
import os


def do_something(in_dict, out_fn, threads):
    print('Processed', in_dict, 'to', out_fn, 'using threads', threads)
    print('  bench_iteration is', snakemake.bench_iteration)
    print('  resources are', snakemake.resources)
    print('  wildcards are', snakemake.wildcards)
    print('  rule is', snakemake.rule)
    print('  scriptdir is', snakemake.scriptdir)
    print('  params are', snakemake.params)


for out in snakemake.output:
    if not os.path.exists(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))

    with open(out, 'w') as sys.stdout:
        do_something(in_dict=snakemake.input,
                     out_fn=out,
                     threads=snakemake.threads)


parameters = dict(snakemake.params)['parameters']
if parameters is not None:
    first_output = snakemake.output[0]
    parent_dir = os.path.dirname(first_output)

    params_file = os.path.join(parent_dir, 'parameters.txt')
    with open(params_file, 'w') as params_file:
        for param in parameters:
            params_file.write(f'{param}\n')



