from activitysim.core import workflow
from activitysim.core import expressions
from activitysim.core.configuration import PydanticBase
import pandas as pd
import numpy as np
import pathlib
import os

@workflow.step()
def empty_model(state: workflow.State) -> None:
    print("This is an empty model")
    return None

@workflow.step()
def count_households(state: workflow.State,
                     households: pd.DataFrame) -> None:
    print("Number of households ", len(households))
    return None

@workflow.step()
def compute_variables_for_households(state: workflow.State,
                                     households: pd.DataFrame,
                                     settings: dict | PydanticBase) -> None:
    # Compute a bunch of variables that also require the persons dataset
    if isinstance(settings, PydanticBase):
        settings = settings.dict()    
    expressions.assign_columns(state, households, model_settings=settings.get("household_variables"))
    print("Average number of children of age < 18 = ", households["num_children"].mean())
    print("Average number of children of age < 13 = ", households["persons_under_13"].mean())
    print ("Starting year of simulation = ", households["start_year"].min())
    return None

@workflow.step()
def add_new_households(state: workflow.State,
                       households: pd.DataFrame) -> None:
    n = 10
    sample = households.sample(n)
    # change the index, i.e. household_id
    sample.index = np.arange(households.index.max() + 1, households.index.max() + n + 1)
    # set current year of simulation
    sample["year"] = state.get_injectable("year")    
    # concatenate
    state.extend_table("households", sample)
    return None

@workflow.step()
def remove_households(state: workflow.State,
                      households: pd.DataFrame) -> None:
    n = 2
    sample = households.sample(n)
    households = households.drop(sample.index)
    state.add_table("households", households)
    return None

@workflow.step()
def write_tables_for_sim_year(state: workflow.State,
                      households: pd.DataFrame, 
                      persons: pd.DataFrame) -> None:
    current_year = state.get_injectable("year")
    if isinstance(state.filesystem.output_dir, pathlib.PurePath): 
        output_dir = state.filesystem.output_dir/str(current_year)
    else: 
        output_dir = state.filesystem.working_dir/f"output/{current_year}"

    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    if current_year == state.get_global_constants()['END_YEAR']:
        # If this is the last year of the simulation, write out all tables
        print(f"Writing households and persons tables for year {current_year} to {output_dir}")
        households.to_parquet(output_dir/"households.parquet", compression="gzip")
        persons.to_parquet(output_dir/"persons.parquet", compression="gzip")
        print(f"Tables households and persons written to {output_dir}")

    else:
        # If this is not the last year of the simulation, write out only the persons and households table
        print(f"Writing households table for year {current_year} to {output_dir}")
        households.to_parquet(output_dir/"households.parquet", compression="gzip")
        persons.to_parquet(output_dir/"persons.parquet", compression="gzip")
        print(f"Table households written to {output_dir}")
    


# @workflow.step()
# def add_column_to_households(state: workflow.State,
#                       households: pd.DataFrame) -> None:
#     # Add a new column to the households table
#     households["year"] = state.get_injectable("year")
#     state.add_table("households", households)
#     return None
