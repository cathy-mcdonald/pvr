import sys
import glob
import ConvertRecordedTS

def convert_all_recorded_ts(pvr_dir):
  ts_dir = pvr_dir + "\\TS"
  file_list = glob.glob(ts_dir + "\\*.ts")
  for file_path in file_list:
    ConvertRecordedTS.convert_recorded_ts(pvr_dir, file_path, pvr_dir + "\\convert\\ConversionLog.txt")

if __name__ == "__main__":
  convert_all_recorded_ts(sys.argv[1])