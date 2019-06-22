from logHelper import ExecuteWithLogs
from postprocessingHelper import Generate3dSplay
import os
import sys

os.chdir("./data")
log_file_path = "log.txt"
ExecuteWithLogs("Splay 3D generation", log_file_path, lambda _ = None: Generate3dSplay())   

