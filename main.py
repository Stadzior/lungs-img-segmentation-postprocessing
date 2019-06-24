from logHelper import ExecuteWithLogs
from postprocessingHelper import GenerateRawFileFromPngs, Generate3dSplay
import os
import sys

os.chdir("./data")
log_file_path = "log.txt"
files = list(filter(lambda x: x.endswith(".mhd"), os.listdir(".")))
ExecuteWithLogs("Raw file generation", log_file_path, lambda _ = None: GenerateRawFileFromPngs(files))   
#ExecuteWithLogsfile 3D generation", log_file_path, lambda _ = None: Generate3dSplay(files))   
