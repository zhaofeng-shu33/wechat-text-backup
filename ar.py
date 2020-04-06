# read the log file, extract and format the chat-history part
import argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    output_name = args.filename + '.output.txt'
