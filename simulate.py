# Urbansim via ActivitySim

import argparse
import sys
#import logging
#from activitysim.core import inject
#from activitysim.core import config
##from activitysim.core import tracing
#from activitysim.core import pipeline

#from activitysim.core.config import handle_standard_args
#from activitysim.core.tracing import print_elapsed_time


from activitysim.cli.run import add_run_args, run

#from activitysim import abm
import urbansim.models

if __name__ == "__main__":

    #handle_standard_args()
    
    ##tracing.config_logger()
    
    #t0 = print_elapsed_time()
    
    #logger = logging.getLogger('urbansim') 
    
    #settings = inject.get_injectable("settings")
    
    #models = settings.get("models")
    
    #pipeline.run(models=models)
    
    #pipeline.close_pipeline()
    
    #t0 = ("all models", t0)    


    parser = argparse.ArgumentParser()
    add_run_args(parser)
    args = parser.parse_args()

    sys.exit(run(args))
