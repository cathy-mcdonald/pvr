import sys
import os
import datetime
import glob
import MergeToMKV
import Demux

convert_dir = "E:\\PVR\\convert"
output_dir = "E:\\PVR\\MKV"
done_dir = "E:\\PVR\\TS\\Done"
failed_dir = "E:\\PVR\\TS\\Failed"

def convert_recorded_ts(ts_file_path, log_file_path):

  ts_file_name = os.path.basename(ts_file_path)

  log_file = open(log_file_path, "a+")
  log_file.write(str(datetime.datetime.now()) + " - START conversion of " + ts_file_name + "\n")
  Demux.demux(ts_file_path, convert_dir, log_file)
  output_file_path = output_dir + "\\" + os.path.splitext(ts_file_name)[0] + ".mkv"
  return_code = MergeToMKV.mux(output_file_path, convert_dir, log_file)

  log_file.write("Return code:{0}\n".format(return_code))

  xml_file_path = os.path.splitext(ts_file_path)[0] + ".xml"
  if return_code in [0, 1]:
    if os.path.isfile(output_file_path):
	  os.rename(ts_file_path, done_dir + "\\" + os.path.basename(ts_file_name))
	  os.rename(xml_file_path, output_dir + "\\" + os.path.basename(xml_file_path))
    else:
	  os.rename(ts_file_path, failed_dir + "\\" + os.path.basename(ts_file_name))
	  os.rename(xml_file_path, failed_dir + "\\" + os.path.basename(xml_file_path))
  else:
    os.rename(ts_file_path, failed_dir + "\\" + os.path.basename(ts_file_name))
    os.rename(xml_file_path, failed_dir + "\\" + os.path.basename(xml_file_path))
  
  # Clean up temporary files
  file_list = glob.glob(convert_dir + "\\" + os.path.splitext(ts_file_name)[0] + "_PID*.*")
  file_list.extend(glob.glob(convert_dir + "\\" + os.path.splitext(ts_file_name)[0] + ".*"))
  for file_path in file_list:
    try:
      os.remove(file_path)
    except:
      log_file.write("Error deleting file:{0}\n".format(file_path))

  log_file.write(str(datetime.datetime.now()) + " - COMPLETED conversion of " + ts_file_name + "\n")
  log_file.close()


if __name__ == "__main__":
  convert_recorded_ts(sys.argv[1], "E:\\PVR\\convert\\PythonLog.txt")