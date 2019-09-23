import sys
import glob
import psutil
import os
import ConvertRecordedTS

def convert_all_recorded_ts(pvr_dir):
  # Process all ts files in TS directory
  ts_dir = pvr_dir + "\\TS"
  file_list = glob.glob(ts_dir + "\\*.ts")
  for file_path in file_list:
    ConvertRecordedTS.convert_recorded_ts(pvr_dir, file_path, pvr_dir + "\\convert\\ConversionLog.txt")

if __name__ == "__main__":
  # Check if this script is already running
  for proc in psutil.process_iter():
    try:
      if (proc.name().lower() == "python.exe") and ("AllRecordedTS.py" in proc.cmdline()) and (proc.pid != os.getpid()):
        print("Script already running!")
        exit()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      pass
  
  convert_all_recorded_ts(sys.argv[1])