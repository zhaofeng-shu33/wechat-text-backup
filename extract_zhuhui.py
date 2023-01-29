import os
from datetime import datetime
import html
from bs4 import BeautifulSoup
import shutil
import warnings
import sqlite3
import re
warnings.filterwarnings("ignore", message=".*HTML parser.*")
input_root = 'C:/Users/zhaofeng/Apple/MobileSync/Backup/00008030-000C64C63446402E'
my_id = 'fc1faa899a951bf80f7755c8e40ca392'
micro_msg_key = 'Documents/{0}/DB/WCDB_Contact.sqlite'.format(my_id)
message_sqlite_list = []
conn = sqlite3.connect('{0}/Manifest.db'.format(input_root))
c = conn.cursor()
c.execute("SELECT fileID,relativePath FROM Files WHERE domain='AppDomain-com.tencent.xin'")
micro_msg_path = ''
for entry in c.fetchall():
    match_result = re.match('^Documents/fc1faa899a951bf80f7755c8e40ca392/DB/message_([1-9]).sqlite$', entry[1])
    if match_result is not None:
        message_sqlite_list.append((match_result.group(), entry[0]))
        continue
    if entry[1] == micro_msg_key:
        micro_msg_path = entry[0]
# print(message_sqlite_list, micro_msg_path)
message_sqlite_list.sort(key=lambda x:x[0])
cursor_list = []
for index, message in message_sqlite_list:
    data_base_filename = input_root + "/" + message[:2] + "/" + message
    print(index, message)
    conn = sqlite3.connect(data_base_filename)
    cursor_list.append(conn.cursor())

table = 'a008711ad1fdc9f567f38778552cbbd3'
statement = 'SELECT CreateTime,Message,Des,Type,MesLocalID FROM Chat_a008711ad1fdc9f567f38778552cbbd3;'


displayname = '赵丰与朱慧'
_html = "<!DOCTYPE html PUBLIC ""-//W3C//DTD XHTML 1.0 Transitional//EN"" ""http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"">"
_html += "<html xmlns=""http://www.w3.org/1999/xhtml""><head><meta http-equiv=""Content-Type"" content=""text/html; charset=utf-8"" /><title>" + displayname + " - 微信聊天记录</title></head>"
_html += "<body><table width=""600"" border=""0"" style=""font-size:12px;border-collapse:separate;border-spacing:0px 20px;word-break:break-all;table-layout:fixed;word-wrap:break-word;"" align=""center"">"

my_portaint = 'Feishu20220613-201140.jpg'
target_portaint = 'Feishu20220613-201131.jpg'
myself_DisplayName = '赵丰'
friend_DisplayName = '朱慧'
_id = 'zh2512382436'
root_dir = 'E:/wechat_out/fc1faa899a951bf80f7755c8e40ca392/'

def RemoveCdata(st):
    return st

for index, cursor in enumerate(cursor_list):
    print(index)
    try:
        cursor.execute(statement)
    except sqlite3.OperationalError:
        continue
    for entry in cursor.fetchall():
        unixtime = entry[0]
        message = entry[1]
        des = entry[2]
        type = entry[3]
        msgid = str(entry[4])

        if type == 10002:
            # revoke message
            continue                           
        if type == 10000:
            _html += "<tr><td width=""80"">&nbsp;</td><td width=""100"">&nbsp;</td><td>系统消息: " + message + "</td></tr>"
            continue
        ts = ""
                
        if des == 0:
            ts += "<tr><td width=""80"" align=""center""><img src=""Portrait/" + my_portaint +  ' width="50" height="50" /><br />' + myself_DisplayName + "</td>"
        else:
            ts += "<tr><td width=""80"" align=""center""><img src=""Portrait/" + target_portaint + ' width="50" height="50" /><br />' + friend_DisplayName + "</td>"
                    
        if type == 34:
            audio_filename =  root_dir + _id + "_files/" + msgid + ".mp3"
            if not os.path.exists(audio_filename):
                message = "[语音]"
            else:
                message = "<audio controls><source src=\"" + _id + "_files/" + msgid + ".mp3\" type=\"audio/mpeg\"><a href=\"" + _id + "_files/" + msgid + ".mp3\">播放</a></audio>"
        elif type == 47:
            match = BeautifulSoup(message).find("emoji").get('cdnurl')
            if (match):
                localfile = RemoveCdata(match)
                match2 = localfile.split('/')[-2]
                if (not match2):
                    import pdb
                    pdb.set_trace()
                    # localfile = RandomString(10)
                else:
                    localfile = match2
                # emoji_file_name = root_dir + "Emoji/" + localfile + ".gif"
                # emoji_target_directory = root_dir + "Emoji_2/" + localfile + ".gif"
                # shutil.copy(emoji_file_name, emoji_target_directory)
                # emojidown.Add(new DownloadTask() { url = match.group(1), filename = localfile + ".gif" })
                message = "<img src=\"Emoji_2/" + localfile + ".gif\" style=\"max-width:100px;max-height:60px\" />"
            else:
                message = "[表情]"
        elif type == 62 or type == 43:    
            hasthum = os.path.exists(root_dir + _id + "_files/" + msgid + "_thum.jpg")
            hasvid = os.path.exists(root_dir + _id + "_files/" + msgid + ".mp4")
            if (hasthum and hasvid):
                message = "<video controls poster=\"" + _id + "_files/" + msgid + "_thum.jpg\"><source src=\"" + _id + "_files/" + msgid + ".mp4\" type=\"video/mp4\"><a href=\"" + _id + "_files/" + msgid + ".mp4\">播放</a></video>"
            elif (hasthum):
                message = "<img src=\"" + _id + "_files/" + msgid + "_thum.jpg\" /> （视频丢失）"
            elif (hasvid):
                message = "<video controls><source src=\"" + _id + "_files/" + msgid + ".mp4\" type=\"video/mp4\"><a href=\"" + _id + "_files/" + msgid + ".mp4\">播放</a></video>"
            else:
                message = "[视频]"
        elif type == 50:
            message = "[视频/语音通话]"
        elif type == 3:
            hasthum = os.path.exists(root_dir + _id + "_files/" + msgid + "_thum.jpg")
            haspic = os.path.exists(root_dir + _id + "_files/" + msgid + ".jpg")
            if (hasthum and haspic):
                message = "<a href=\"" + _id + "_files/" + msgid + ".jpg\"><img src=\"" + _id + "_files/" + msgid + "_thum.jpg\" style=\"max-width:100px;max-height:60px\" /></a>"
            elif (hasthum):
                message = "<img src=\"" + _id + "_files/" + msgid + "_thum.jpg\" style=\"max-width:100px;max-height:60px\" />"
            elif (haspic):
                message = "<img src=\"" + _id + "_files/" + msgid + ".jpg\" style=\"max-width:100px;max-height:60px\" />"
            else:
                message = "[图片]"
        elif type == 48:
            match1 = re.search("x ?= ?""(.+?)""", message)
            match2 = re.search("y ?= ?""(.+?)""", message)
            match3 = re.search("label ?= ?""(.+?)""", message)
            if (match1 and match2 and match3):
                message = "[位置 (" + RemoveCdata( match2.group(1)) + "," + RemoveCdata(match1.group(1)) + ") " + RemoveCdata(match3.group(1)) + "]"
            else:
                message = "[位置]"
        elif type == 49:
            if (message.find("<type>2001<") >= 0):
                message = "[红包]"
            elif (message.find("<type>2000<") >= 0):
                message = "[转账]"
            elif (message.find("<type>17<") >= 0):
                message = "[实时位置共享]"
            elif (message.find("<type>6<") >= 0):
                match1 = re.search("<fileext>(.+?)<\/fileext>", message)
                match2 = re.search("<title>(.+?)<\/title>", message)
                if (match1 and match2):
                    hasfile = os.path.exists(root_dir + _id + "_files/" + match2.group(1))
                    if (hasfile):
                        message = "<a href=\"" + _id + "_files/" + match2.group(1) + "\">" + match2.group(1) + "</a>"
                    else:
                        message = match2.group(1) + "(文件丢失)"
                else:
                    message = "[文件]"
            else:
                match1 = BeautifulSoup(message).find_all("title")[0].text
                match2 = re.search("<des>(.*?)<\/des>", message)
                match3 = re.search("<url>(.+?)<\/url>", message)
                match4 = re.search("<thumburl>(.+?)<\/thumburl>", message)
                if match1 and match3:
                    message = ""
                    if match4:
                        message += "<img src=\"" + RemoveCdata(match4.group(1)) + "\" style=\"float:left;max-width:100px;max-height:60px\" />"
                    message += "<a href=\"" + RemoveCdata(match3.group(1)) + "\"><b>" + RemoveCdata(match1) + "</b></a>"
                    if match2:
                        message += "<br />" + RemoveCdata(match2.group(1))
                else:
                    try:
                        sub_message = html.unescape(BeautifulSoup(message).find_all("content")[-1].text)
                        if sub_message.find('xml') >= 0 or sub_message.find('appmsg') >= 0:
                            try:
                                if BeautifulSoup(sub_message).find("img"):
                                    quote = "[图片]"
                                elif BeautifulSoup(sub_message).find('videomsg'):
                                    quote = "[视频]"
                                else:
                                    quote = BeautifulSoup(sub_message).find_all("title")[0].text
                            except Exception as e:
                                import pdb
                                pdb.set_trace()
                        else:
                            quote = sub_message
                        message = quote + "<br />------------<br />"  + match1 + "<br/>&nbsp;"
                    except Exception as e:
                        import pdb
                        pdb.set_trace()
                        message = "[链接]"
        elif type == 42:
            match1 = re.search("nickname ?= ?\"(.+?)\"", message)
            match2=re.search("smallheadimgurl ?= ?\"(.+?)\"", message)
            if match1:
                message = ""
                if(match2):
                    message+= "<img src=\"" + RemoveCdata(match2.group(1)) + "\" style=\"float:left;max-width:100px;max-height:60px\" />"
                message += "[名片] " + RemoveCdata(match1.group(1))
            else:
                message = "[名片]"
        else:
            message = html.escape(message)
            if message.find("- - - - - - - - - - - - - - -") >= 0:
                message = message.replace("- - - - - - - - - - - - - - -", "<br/>- - - - - - - - - - - - - - -<br/>")
            if message.find("我们换本别的书吧x") >= 0:
                import pdb
                pdb.set_trace()
        ts += "<td width=""100"" align=""center"">" + datetime.fromtimestamp(unixtime).strftime("%Y/%m/%d %H:%M:%S").replace(" ","<br />") + "</td>"
        ts += "<td>" + message + "</td></tr>"
        _html += ts

_html += "</body></html>"
with open(os.path.join(root_dir, "test.html"), 'w', encoding='utf-8') as f:
    f.write(_html)
