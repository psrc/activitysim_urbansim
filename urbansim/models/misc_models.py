from activitysim.core import workflow
from activitysim.core import expressions
from activitysim.core.configuration import PydanticBase
import pandas as pd
import numpy as np

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
    return None

@workflow.step()
def add_new_households(state: workflow.State,
                       households: pd.DataFrame) -> None:
    n = 10
    sample = households.sample(n)
    # change the index, i.e. household_id
    sample.index = np.arange(households.index.max() + 1, households.index.max() + n + 1)
    # concatenate
    households = pd.concat([households, sample])
    return None

