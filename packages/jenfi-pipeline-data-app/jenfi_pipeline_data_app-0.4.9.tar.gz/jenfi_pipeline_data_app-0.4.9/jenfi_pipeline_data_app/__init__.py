__version__ = "0.4.9"

# from ._pdoc import __pdoc__
from .app import Application
import os

PipelineDataApp = Application()

PipelineDataApp.boot()

core_app_name = os.getenv("CORE_APP_NAME", None)

print()
print()
print(f"Welcome to the Jenfi Data App! v{__version__}")
print(f"{core_app_name}")
print("https://jenfi-eng.github.io/pipeline-data-app")
print(
    "------------------------------------------------------------------------------------"
)
print()
print("!!REQUIRED!! variables in `parameters` tagged cell.")
print()
print(
    "logical_step_name        - ex:   `logical_step_name = 'sg_first_payment_default'`"
)
print("                           This name should be unique to the step+flow you are")
print("                           running.")
print("state_machine_run_id     - ex:   `state_machine_run_id = 5`")
print("                           This allows caching of data to be tied to a specific")
print("                           run based on the run_id. This is useful for")
print("                           reproducing and investigating historical.")
print(
    "------------------------------------------------------------------------------------"
)
print()
print("OPTIONAL variables in `parameters` tagged cell.")
print()
print("disable_cache            - Default: `False`")
print("                           ex:   `disable_cache = True`")
print("                           Disables the cache so queries always hit the DB for")
print("                           newest data.")
print(
    "------------------------------------------------------------------------------------"
)
print()
