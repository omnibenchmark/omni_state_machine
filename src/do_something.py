#! /usr/bin/env python
##
## A benchmarking (fake) step parsing params, inputs and outputs
##
## Started 22 Feb 2024
## Izaskun Mallona

import sys

def do_something(in_dict, out_fn, params_dict, threads):
    print('Processed', in_dict, 'to', out_fn, 'using params', params_dict, 'and threads', threads, '.\n')

for out in snakemake.output:
    with open(out, 'w') as sys.stdout:
        do_something(in_dict = snakemake.input,
                     out_fn = out,
                     params_dict = snakemake.params,
                     threads = snakemake.threads)
