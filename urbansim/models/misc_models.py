from activitysim.core import inject
from activitysim.core import expressions
    
@inject.step()
def empty_model():
    print("This is an empty model")
    return

@inject.step()
def count_households(households):
    print("Number of households ", len(households))
    return

@inject.step()
def compute_variables_for_households(households, settings):
    expressions.assign_columns(households, model_settings=settings.get("household_variables"))
    return
