# script launchered from linux host
# four steps in total
set -e -x
ssh feng@10.1.1.6 "cd source\repos\wechat-text-backup && \"C:\Program Files\Git\bin\bash.exe\" win-upload-script.sh"
bash linux-process-script.sh
python3 extract.py
/usr/local/bin/ossutil64 cp -rf read oss://freiwilliger/wechat/
