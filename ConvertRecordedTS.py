import sys
import os
import datetime
import glob
import TestFile
import MergeToMKV
import Demux


def convert_recorded_ts(pvr_dir, ts_file_path, log_file_path):
  convert_dir = pvr_dir + "\\convert"
  output_dir = pvr_dir + "\\MKV"

  # Stop if ts file is still being written
  if TestFile.file_in_use(ts_file_path):
    return
	
  ts_file_name = os.path.basename(ts_file_path)

  log_file = open(log_file_path, "a+")
  log_file.write(str(datetime.datetime.now()) + " - START conversion of " + ts_file_name + "\n")

  # Deal with duplicate file names  
  output_file_path = output_dir + "\\" + os.path.splitext(ts_file_name)[0] + ".mkv"
  new_ts_file_path = ""
  i = 0
  while os.path.isfile(output_file_path) or os.path.isfile(new_ts_file_path):
    i = i + 1
    output_file_path = output_dir + "\\" + os.path.splitext(ts_file_name)[0] + "_" + str(i) + ".mkv"
    new_ts_file_path = os.path.splitext(ts_file_path)[0] + "_" + str(i) + ".ts" 
  if (i > 0):
    rename_files(ts_file_path, new_ts_file_path)
    ts_file_path = new_ts_file_path
    ts_file_name = os.path.splitext(ts_file_name)[0] + "_" + str(i) + ".ts"
  
  # Demux file into video, audio and subtitle streams
  Demux.demux(ts_file_path, convert_dir, log_file)
  
  # Mux into Matroska file format
  output_file_path = output_dir + "\\" + os.path.splitext(ts_file_name)[0] + ".mkv"
  return_code = MergeToMKV.mux(output_file_path, convert_dir, log_file)

  log_file.write("Return code:{0}\n".format(return_code))

  move_files(ts_file_path, pvr_dir, (return_code in [0, 1]) and os.path.isfile(output_file_path))
  
  cleanup(convert_dir, ts_file_name, log_file)

  log_file.write(str(datetime.datetime.now()) + " - COMPLETED conversion of " + ts_file_name + "\n")
  log_file.close()

# Rename input files
def rename_files(ts_file_path, new_ts_file_path):
  xml_file_path = os.path.splitext(ts_file_path)[0] + ".xml"
  new_xml_file_path = os.path.splitext(new_ts_file_path)[0] + ".xml"
  os.rename(ts_file_path, new_ts_file_path)
  if os.path.isfile(xml_file_path):
    os.rename(xml_file_path, new_xml_file_path)

# Move ts and xml file to appropriate directory based on success of conversion
def move_files(ts_file_path, pvr_dir, success):
  done_dir = pvr_dir + "\\TS\\Done"
  failed_dir = pvr_dir + "\\TS\\Failed"
  output_dir = pvr_dir + "\\MKV"
  
  xml_file_path = os.path.splitext(ts_file_path)[0] + ".xml"
  move_to_ts_file_path = done_dir + "\\" + os.path.basename(ts_file_path)
  move_to_xml_file_path = output_dir + "\\" + os.path.basename(xml_file_path)
  
  if not success:
    move_to_ts_file_path = failed_dir + "\\" + os.path.basename(ts_file_path)
    move_to_xml_file_path = failed_dir + "\\" + os.path.basename(xml_file_path)

  # Deal with duplicate file names
  i = 0
  new_ts_path = move_to_ts_file_path
  while os.path.isfile(new_ts_path):
    i = i + 1
    new_ts_path = os.path.splitext(move_to_ts_file_path)[0] + "_" + str(i) + ".ts"
  if (i > 0):
    move_to_ts_file_path = new_ts_path
    move_to_xml_file_path = os.path.splitext(new_ts_path)[0] + ".xml"
	  
  os.rename(ts_file_path, move_to_ts_file_path)
  if os.path.isfile(xml_file_path):
    os.rename(xml_file_path, move_to_xml_file_path)


# Delete temporary files
def cleanup(convert_dir, ts_file_name, log_file):
  file_list = glob.glob(convert_dir + "\\" + os.path.splitext(ts_file_name)[0] + "_PID*.*")
  file_list.extend(glob.glob(convert_dir + "\\" + os.path.splitext(ts_file_name)[0] + ".*"))
  for file_path in file_list:
    try:
      os.remove(file_path)
    except:
      log_file.write("Error deleting file:{0}\n".format(file_path))

if __name__ == "__main__":
  convert_recorded_ts("E:\\PVR", sys.argv[1], "E:\\PVR\\convert\\PythonLog.txt")