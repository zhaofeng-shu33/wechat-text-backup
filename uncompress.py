import pdb
import re
import html
from ar import parse_single_msg
FILE_TYPE = 6
FILE_TYPE_2 = 0
URL_TYPE = 5
LIVE_TYPE = 60
APP_TYPE = 3
APP_TYPE_2 = 33
CHAT_HISTORY_TYPE = 19
MINI_PROGRAM_TYPE = 36
REFER_MESSAGE_TYPE = 57
VIEW_TYPE = 1
EXTERNAL_EMOJI = 8
ONLINE_VIDEO_TYPE = 51
ONLINE_VIDEO_TYPE_2 = 54
RED_PACKET_TYPE = 2003
SOLITAIRE_TYPE = 53 # Chinese: people chain
MONEY_TRANSFER = 2000
LOCATION_SHARING_TYPE = 17
FAVORITE_SHARING = 24

def extract_url(byte_str):
    uncompressed_content = uncompress(byte_str)
    match_obj = re.search('<url>(.*)</url>', uncompressed_content)
    if match_obj is None:
        return 'Unknown Link'
    return match_obj.group(1)

def extract_content(byte_str, subtype):
    uncompressed_content = uncompress(byte_str)
    if subtype == FILE_TYPE or subtype == FILE_TYPE_2:
        match_obj = re.search('<title>(.*)</title>', uncompressed_content)    
        content = match_obj.group(1)
    elif subtype == URL_TYPE:
        match_obj = re.search('<url>(.*)</url>', uncompressed_content)
        content = match_obj.group(1)
    elif subtype == LIVE_TYPE:
        content = '[live]'
    elif subtype == CHAT_HISTORY_TYPE:
        match_obj = re.search('<recorditem>(.*)</recorditem>', uncompressed_content)
        try:
            _html = match_obj.group(1)
            _html = html.unescape(_html)
            content = parse_single_msg(_html)
        except:
            content = '[chat history]'
    elif subtype == MINI_PROGRAM_TYPE:
        content = '[mini program]'
    elif subtype == REFER_MESSAGE_TYPE:
        content = '[refer message]'
    elif subtype == VIEW_TYPE:
        match_obj = re.search('<des>(.*)</des>', uncompressed_content)
        try:
            content = match_obj.group(1)
        except:
            content = '[view type]'
    elif subtype == APP_TYPE or subtype == APP_TYPE_2:
        content = '[app message]'
    elif subtype == EXTERNAL_EMOJI:
        content = '[external emoji]'
    elif subtype == ONLINE_VIDEO_TYPE or subtype == ONLINE_VIDEO_TYPE_2:
        content = '[online video]'
    elif subtype == RED_PACKET_TYPE:
        content = '[red packet]'
    elif subtype == SOLITAIRE_TYPE:
        content = '[people chain]'
    elif subtype == MONEY_TRANSFER:
        content = '[money transfer]'
    elif subtype == LOCATION_SHARING_TYPE:
        content = '[location sharing]'
    elif subtype == FAVORITE_SHARING:
        content = '[favorite sharing]'
    else:
        content = '[unknown link type]'
    return content

def uncompress(byte_str, verbose=False):
    # compress data in LZ4 format
    offset = byte_str[0] >> 4 # possible value: 14
    next_backward_length = 4 + byte_str[0] - offset * 16
    pointer = 1
    if offset == 15:
        while byte_str[pointer] == 255:
            pointer += 1
            offset += 255
        offset += byte_str[pointer]
        pointer += 1
    valid_bytes = byte_str[pointer:pointer + offset]
    pointer += offset
    total_len = len(byte_str)
    while pointer < total_len:   
        backward_length = next_backward_length
        distance = int.from_bytes(byte_str[pointer:pointer + 2], 'little')
        pointer += 2
        if backward_length == 19:
            while byte_str[pointer] == 255:
                pointer += 1
                backward_length += 255
            backward_length += byte_str[pointer]
            pointer += 1
        length_info = byte_str[pointer]
        if length_info < 240: # 0b11110000
            pointer += 1
            forward_length = length_info >> 4
            next_backward_length = length_info - forward_length * 16 + 4
        else:
            forward_length = 15
            while byte_str[pointer + 1] == 255:
                pointer += 1
                forward_length += 255
            forward_length += byte_str[pointer + 1]
            next_backward_length = length_info - (length_info >> 4) * 16 + 4
            pointer += 2
        if verbose:
            print(hex(pointer), forward_length)
        if distance == 1:
            for _ in range(backward_length):
                valid_bytes += valid_bytes[-1 :]
        else:
            while -1 * distance + backward_length > 0:
                valid_bytes += valid_bytes[-1 * distance : -1]
                backward_length -= (distance - 1)
            if -1 * distance + backward_length == 0:
                valid_bytes += valid_bytes[-1 * distance :]
            else:
                valid_bytes += valid_bytes[-1 * distance : -1 * distance + backward_length]
        if forward_length > 0:
            valid_bytes += byte_str[pointer: pointer + forward_length]
        pointer += forward_length
        if verbose:
            try:
                print(valid_bytes.decode('utf-8'))
            except:
                pdb.set_trace()
    try:
        return valid_bytes.decode('utf-8')
    except:
        open('a3.bin', 'wb').write(byte_str)
        valid_bytes.decode('utf-8')

if __name__ == '__main__':
    f = open('a2.bin', 'rb')
    st = f.read()
    print(uncompress(st, verbose=True))
