import azureml.core
from azureml.core import Workspace

# check core SDK version number
print("Azure ML SDK Version: ", azureml.core.VERSION)

ws = Workspace.from_config()
print(ws)
#print(ws.name, ws.location, ws.resource_group, sep='\t')