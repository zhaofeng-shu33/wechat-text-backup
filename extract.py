# this script is used to extract chathistory of one chatroom
import argparse
import os
import sqlite3
from datetime import datetime
import pdb

TEXT_TYPE = 1
EXTERNAL_EMOJI_TYPE = 47
REVOKE_TYPE = 10000
IMAGE_TYPE = 3
LINK_TYPE = 49
POSITION_TYPE = 48
VIDEO_TYPE = 43
AUDIO_TYPE = 34
CARD_TYPE = 42
FRIEND_REQUEST_TYPE = 37
CALL_TYPE = 50

def get_wx_id(wx_byte):
    wx_uni = wx_byte.decode('utf-8', 'replace')
    for index, i in enumerate(wx_uni):
        if not i.isprintable():
            continue
        start_index = index
        break
    for index, i in enumerate(wx_uni[start_index+1:]):
        if i.isprintable():
            continue
        end_index = index
        break
    return wx_uni[start_index:end_index]

def get_message_list(cursor, chatroom_id):
    message_list = [] # speaker_id, time-obj, message-text
    sql_statement = 'select BytesExtra, CreateTime, StrContent, Type, IsSender from MSG where StrTalker = "%s";' % chatroom_id
    cursor.execute(sql_statement)
    for entry in cursor.fetchall():
        main_type = entry[3]
        is_sender = entry[4]
        if main_type == REVOKE_TYPE:
            continue
        bytes_extra_obj = entry[0]
        if is_sender == 1:
            wx_id = 'me'
        elif chatroom_id.find('chatroom') < 0:
            wx_id = chatroom_id
        else:
            try:
                wx_id = get_wx_id(bytes_extra_obj)
            except Exception as e:
                pdb.set_trace()
        _timestamp = entry[1]
        dt_object = datetime.fromtimestamp(_timestamp)        
        if main_type == EXTERNAL_EMOJI_TYPE:
            _content = '[external emoji]'
        elif main_type == TEXT_TYPE:
            _content = entry[2]
        elif main_type == IMAGE_TYPE:
            _content = '[image]'
        elif main_type == LINK_TYPE:
            _content = '[link]'
        elif main_type == POSITION_TYPE:
            _content = '[position]'
        elif main_type == VIDEO_TYPE:
            _content = '[video]'
        elif main_type == AUDIO_TYPE:
            _content = '[audio]'
        elif main_type == CARD_TYPE:
            _content = '[card]'
        elif main_type == FRIEND_REQUEST_TYPE:
            _content = '[friend request]'
        elif main_type == CALL_TYPE:
            _content = '[call]'
        else:
            pdb.set_trace()
        message_list.append([wx_id, dt_object, _content])
    return message_list

def write_message_list(message_list, output_file):
    st = ''
    for message_entry in message_list:
        wx_id = message_entry[0]
        time_obj = message_entry[1]
        _content = message_entry[2]
        st += time_obj.strftime("%Y-%m-%d, %H:%M:%S")
        st += ' : ' + wx_id + '\n\t'
        st += _content + '\n\n'
    with open(output_file, 'w') as f:
        f.write(st)

def get_contact_dic(cursor):
    sql_statement = 'select Remark, NickName, UserName from Contact;'
    cursor.execute(sql_statement)
    dic = {}
    for entry in cursor.fetchall():
        remark = entry[0]
        nick_name = entry[1]
        wx_id = entry[2]
        if remark == '':
            _name = nick_name
        else:
            _name = remark
        dic[wx_id] = _name
    return dic

def translate_name(message_list, dic):
    for message_entry in message_list:
        wx_id = message_entry[0]
        if wx_id == 'me':
            continue
        translated_name = dic.get(wx_id)
        if translated_name:
            message_entry[0] = translated_name

def get_chatroom_list(cursor):
    chatroom_list = []
    sql_statement = 'select strUsrName from Session;'
    cursor.execute(sql_statement)
    for entry in cursor.fetchall():
        chatroom_list.append(entry[0])
    return chatroom_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='Multi/MSG0.db.dec.db')
    parser.add_argument('--micro_filename', default='MicroMsg.db.dec.db')
    parser.add_argument('--working_dir', default='dec_db')
    parser.add_argument('--output_dir', default='read')
    parser.add_argument('--chatroom_id', default='')
    args = parser.parse_args()
    cwd = os.getcwd()
    os.chdir(args.working_dir)
    if os.path.exists(args.micro_filename):
        conn_contact = sqlite3.connect(args.micro_filename)
        cursor_contact = conn_contact.cursor()
        contact_dic = get_contact_dic(cursor_contact)
        if args.chatroom_id == '':
            processing_chatlist = True
        else:
            processing_chatlist = False
    else:
        contact_dic = {}
        processing_chatlist = False
    conn = sqlite3.connect(args.filename)
    cursor = conn.cursor()
    if processing_chatlist:
        chatroom_list = get_chatroom_list(cursor_contact)
    else:
        chatroom_list = [args.chatroom_id]
    os.chdir(cwd)
    for chatroom in chatroom_list:
        message_list = get_message_list(cursor, chatroom)
        if contact_dic:
            translate_name(message_list, contact_dic)
        alias_name = chatroom
        if contact_dic and contact_dic.get(alias_name):
            alias_name = contact_dic[alias_name]
        alias_name = alias_name.replace(' ', '').replace('/', '')
        output_file = os.path.join(args.output_dir, alias_name + '.md')    
        write_message_list(message_list, output_file)
