E:
REM recreate directory structure
mkdir "\PVR"
REM where live recordings go, .ts files:
mkdir "\PVR\TS"
REM where failed conversions from .ts to .mkv go:
mkdir "\PVR\TS\Failed"
REM where converted files are finally sent, ready to be watched over the network
mkdir "\PVR\MKV"
REM temp directory
mkdir "\PVR\convert"

del /q C:\ProgramData\Cypheros\TsDoctor2\Temp\*
call python "\PVR\scripts\AllRecordedTS.py" "E:\PVR"
