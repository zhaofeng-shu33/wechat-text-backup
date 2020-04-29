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
        else:
            try:
                wx_id = bytes_extra_obj.split(b'\x1a')[1].split(b'\x13')[1].decode('ascii')
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
        translated_name = dic.get(message_entry[0])
        if translated_name:
            message_entry[0] = translated_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='Multi/MSG0.db.dec.db')
    parser.add_argument('--micro_filename', default='MicroMsg.db.dec.db')
    parser.add_argument('--working_dir', default='dec_db')
    parser.add_argument('--output_dir', default='read')
    parser.add_argument('chatroom_id')
    args = parser.parse_args()
    cwd = os.getcwd()
    os.chdir(args.working_dir)
    if os.path.exists(args.micro_filename):
        conn_contact = sqlite3.connect(args.micro_filename)
        cursor_contact = conn_contact.cursor()
        contact_dic = get_contact_dic(cursor_contact)
    else:
        contact_dic = {}
    conn = sqlite3.connect(args.filename)
    cursor = conn.cursor()
    message_list = get_message_list(cursor, args.chatroom_id)
    if contact_dic:
        translate_name(message_list, contact_dic)
    output_file = os.path.join(args.output_dir, args.chatroom_id + '.md')
    os.chdir(cwd)
    write_message_list(message_list, output_file)
