import re
import pdb

def guess_length_for_url(start, valid_bytes, remaining_bytes):
    if valid_bytes[start : start + 5] == b'&amp;':
        return 5
    for i in range(1, 10):
        if valid_bytes[start + i : start + 5 + i] == b'&amp;':
            return i + 5
    if valid_bytes.find(b'__biz') > 0:
        return 1
    raise ValueError('not found')

def extract_url(byte_str):
    offset = 256 - byte_str[0]  # possible value: 14
    first_offset = byte_str[1] + offset
    valid_bytes = byte_str[2:first_offset + 3]
    total_len = len(byte_str)
    pointer = byte_str.find(b'http://mp.weixin')
    if pointer < 0:
        return '[Unknown Link]'
    next_pointer = byte_str.find(b'\x00', pointer + 1)
    valid_bytes = byte_str[pointer:next_pointer - 1]
    pointer = next_pointer - 1
    while pointer < total_len:
        if re.search(b'sn=[A-Za-z0-9]+&amp;', valid_bytes):
            break
        distance = int.from_bytes(byte_str[pointer:pointer + 2], 'little')
        pointer += 2
        length_info = byte_str[pointer]
        if length_info < 240: # 0b11110000
            pointer += 1
            forward_length = length_info >> 4
            backward_length = guess_length_for_url(len(valid_bytes) - distance, valid_bytes)
        else:
            forward_length = byte_str[pointer + 1] + offset + 1
            backward_length = guess_length_for_url(len(valid_bytes) - distance, valid_bytes)
            pointer += 2
        valid_bytes += valid_bytes[-1 * distance : -1 * distance + backward_length]
        if forward_length > 0:
            valid_bytes += byte_str[pointer: pointer + forward_length]
        pointer += forward_length
    try:
        url = valid_bytes.decode('utf-8').split('&amp;chksm')[0]
    except:
        pdb.set_trace()
    return url

def uncompress(byte_str):
    offset = 256 - byte_str[0]  # possible value: 14
    first_offset = byte_str[1] + offset
    valid_bytes = byte_str[2:first_offset + 3]
    pointer = first_offset + 3
    total_len = len(byte_str)
    while pointer < total_len:
        distance = int.from_bytes(byte_str[pointer:pointer + 2], 'little')
        pointer += 2
        length_info = byte_str[pointer]
        if length_info < 240: # 0b11110000
            pointer += 1
            forward_length = length_info >> 4
            backward_length = length_info - forward_length * 16
            if dic.get((distance, backward_length)):
                print((bin(distance), forward_length, bin(backward_length)), '=>', dic.get((distance, backward_length)))
                backward_length = dic[(distance, backward_length)]
            else:
                print(valid_bytes.decode('utf-8'))
                print(distance, backward_length)
                print(valid_bytes[-1 * distance :])
                import pdb
                pdb.set_trace()
        else:
            forward_length = byte_str[pointer + 1] + offset + 1
            if dic2.get((distance, length_info)):
                print((bin(distance), forward_length, bin(backward_length)), '=>', dic.get((distance, backward_length)))
                backward_length = dic2[(distance, length_info)]
            else:
                print(valid_bytes.decode('utf-8'))
                print(distance, backward_length)
                print(valid_bytes[-1 * distance :])                
                import pdb
                pdb.set_trace()
            pointer += 2
        valid_bytes += valid_bytes[-1 * distance : -1 * distance + backward_length]
        if forward_length > 0:
            valid_bytes += byte_str[pointer: pointer + forward_length]
        pointer += forward_length
    return valid_bytes.decode('utf-8')

if __name__ == '__main__':
    f = open('a.bin', 'rb')
    st = f.read()
    print(extract_url(st))
