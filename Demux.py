import sys
import datetime
import subprocess
import os
import re

projectx_jar = "E:\\Program Files\\Project-X_0.91.0\\ProjectX.jar"
projectx_ini = "E:\\PVR\\scripts\\X.ini"
stream_ids = "0x0030,0x0040,0x0060,0x0061,0x0062,0x0063,0x0064,0x0065,0x0066,0x0067,0x0068,0x0069,0x006A,0x006B,0x006C,0x006D,0x006E,0x006F,0x0204,0x0242,0x02A9,0x0300,0x0301,0x0302,0x0304"
tsdoctor_command = "C:\\Program Files\\Cypheros\\TSDoctor2\\TSDoctor.exe"
ccextractor_command = "C:\\Program Files\\CCExtractor\\ccextractorwin.exe"

def demux_with_projectx(ts_file_path, output_dir, log_file):
  log_file.flush()
  subprocess.call(["java", "-jar", projectx_jar, "-ini", projectx_ini, "-id", stream_ids,
				   "-out", output_dir, "-demux", ts_file_path], stdout=log_file, stderr=log_file)
				   
				   
def demux_with_tsdoctor(ts_file_name, output_dir, log_file):
  log_file.flush()
  subprocess.call([tsdoctor_command, ts_file_name, "Autofix", output_dir + "\\"], stdout=log_file, stderr=log_file)
  fixed_ts_file_name = output_dir + "\\" + os.path.basename(ts_file_name)
  subprocess.call([tsdoctor_command, fixed_ts_file_name, "Autodemux", output_dir + "\\"], stdout=log_file, stderr=log_file)
  # Extract subtitles with CCExtractor
#  subtitle_file_name = output_dir + "\\" + os.path.splitext(os.path.basename(ts_file_name))[0] + ".srt"
#  subprocess.call([ccextractor_command, "-nofc", ts_file_name, "-o", subtitle_file_name], 
#                   stdout=log_file, stderr=log_file)

				   
def demux(ts_file_name, output_dir, log_file):
  channel_name = ""
  
  try:
    xml_file = open(os.path.splitext(ts_file_name)[0] + ".xml", "r")
    log_file.write(str(datetime.datetime.now()) + " - START demux of " + os.path.basename(ts_file_name) + "\n")

    pattern = re.compile("<name>CHANNEL_NAME</name>\s+<value>(.+)</")
    matches = re.findall(pattern, xml_file.read())
    channel_name = matches[0]
    log_file.write("Channel name: {0}\n".format(channel_name))

    xml_file.close()
  except IOError:
    log_file.write("No xml file found")

  if channel_name in ["9Life", "Channel 9 Melbourne", "9Go!", "9Gem", "7 Digital"]:
    demux_with_projectx(ts_file_name, output_dir, log_file)
  else:
    demux_with_tsdoctor(ts_file_name, output_dir, log_file)

  log_file.write(str(datetime.datetime.now()) + " - COMPLETED demux of " + os.path.basename(ts_file_name) + "\n")
	
		
if __name__ == "__main__":
  log_file = open("E:\\PVR\\convert\\DemuxLog.txt", "a+")
  demux(sys.argv[1], "E:\\PVR\\convert", log_file)
  log_file.close()