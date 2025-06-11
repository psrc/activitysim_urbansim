# Run simple models via the ActivitySim pipeline

## Installation of python for activitysim
## following https://activitysim.github.io/activitysim/v1.3.1/users-guide/modelsetup.html
## Needed to downgrade the numba package
# ########################################
# mamba create -n asim python=3.10 activitysim -c conda-forge --override-channels
# conda activate asim
# pip install numba==0.58.1

# For activitysim itself, clone the repo
# https://github.com/psrc/activitysim
# and checkout the branch urbansim

import argparse
import sys
from activitysim import abm
from urbansim.run import add_run_args, run
import urbansim.models

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_run_args(parser)
    args = parser.parse_args()

    sys.exit(run(args))
