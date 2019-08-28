import sys
import os
import datetime
import glob
import subprocess

mkvmerge_command = "C:\\Program Files\\MKVtoolnix\\mkvmerge.exe"

def mux(output_file_path, convert_dir, log_file):
  show_name = os.path.splitext(os.path.basename(output_file_path))[0]
  log_file.write(str(datetime.datetime.now()) + " - START merge of " + show_name + "\n")

  # Find demuxed video file
  video_file = ""
  if os.path.isfile("{0}\\{1}.m2v".format(convert_dir, show_name)):
    video_file = "{0}\\{1}.m2v".format(convert_dir, show_name)
	
  video_files = glob.glob("{0}\\{1}_PID*.m2v".format(convert_dir, show_name))
  if video_files:
    video_file = video_files[0]
	
  video_files = glob.glob("{0}\\{1}_PID*.264".format(convert_dir, show_name))
  if video_files:
    video_file = video_files[0]
  
  # Find demuxed audio file
  audio_file = ""
  if os.path.isfile("{0}\\{1}.mp2".format(convert_dir, show_name)):
    audio_file = "{0}\\{1}.mp2".format(convert_dir, show_name)
	
  audio_files = glob.glob("{0}\\{1}_PID*.mp2".format(convert_dir, show_name))
  if audio_files:
    audio_file = audio_files[0]
	
  # Find demuxed subtitle file
  subtitle_file = ""
  if os.path.isfile("{0}\\{1}.srt".format(convert_dir, show_name)):
    subtitle_file = "{0}\\{1}.srt".format(convert_dir, show_name)
	
  if os.path.isfile("{0}\\{1}.eng.srt".format(convert_dir, show_name)):
    subtitle_file = "{0}\\{1}.eng.srt".format(convert_dir, show_name)
	
  if os.path.isfile("{0}\\{1}[801].srt".format(convert_dir, show_name)):
    subtitle_file = "{0}\\{1}[801].srt".format(convert_dir, show_name)

  if subtitle_file:
    log_file.write("\"{0}\" -o \"{1}\" \"{2}\" \"{3}\" \"{4}\"\n"
	               .format(mkvmerge_command, output_file_path, video_file, audio_file, subtitle_file))
    return_code = subprocess.call(["C:\Program Files\MKVtoolnix\mkvmerge.exe", "-o", output_file_path, 
					               video_file, audio_file, subtitle_file])
  else:
    log_file.write("\"{0}\" -o \"{1}\" \"{2}\" \"{3}\"\n"
	               .format(mkvmerge_command, output_file_path, video_file, audio_file))
    return_code = subprocess.call(["C:\Program Files\MKVtoolnix\mkvmerge.exe", "-o", output_file_path, 
					               video_file, audio_file])

  log_file.write(str(datetime.datetime.now()) + " - COMPLETED merge of " + show_name + "\n")
  
  return return_code
	
	
if __name__ == "__main__":
  log_file = open("E:\\PVR\\convert\\MergeToMKVLog.txt", "a+")
  mux(sys.argv[1], "E:\\PVR\\convert", log_file)
  log_file.close()