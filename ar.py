# read the log file, extract and format the chat-history part
import argparse
from bs4 import BeautifulSoup

def read_log(filename, encoding='gbk'):
    with open(filename, 'rb') as f:
        st = f.read().decode('gbk', errors='ignore')
    return st

def extract_dialog_part(str):
    '''return a Python list of string
    '''
    pos = 0
    Ls = []
    while True:
        pos = str.find('filehelper', pos)
        if pos < 0:
            break
        new_pos = str.find('<?xml', pos)
        if new_pos < 0:
            break
        if new_pos - pos <= 33:
            msg_start = str.find('<msg>', pos)
            msg_end = str.find('</msg>', pos)
            Ls.append(str[msg_start:msg_end+6])
        pos += 1
    return Ls

def parse_single_msg(msg_str):
    s = BeautifulSoup(msg_str)
    s_i = BeautifulSoup(s.recorditem.text)
    output_str = ''
    for d in s_i.find_all('dataitem'):
        time = d.sourcetime.text
        name = d.sourcename.text
        content = d.datadesc.text
        output_str + '{0} {1}:{2}\n'.format(time, name, content)
    return output_str

def parse_all_msg(msg_list):
    output_str = ''
    for msg_str in msg_list:
        output_str += parse_single_msg(msg_str)
        output_str += '\n'
    return output_str

def parse_and_save(filename):
    st = read_log(filename)
    Ls = extract_dialog_part(st)
    output_str = parse_all_msg(Ls)
    output_name = args.filename + '.output.txt'
    with open(output_name, 'w') as f:
        f.write(output_str)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    parse_and_save(args.filename)