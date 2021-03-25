import pdb
import re
def extract_url(byte_str):
    uncompressed_content = uncompress(byte_str)
    match_obj = re.search('<url>(.*)</url>', uncompressed_content)
    if match_obj is None:
        return 'Unknown Link'
    return match_obj.group(1)

def uncompress(byte_str):
    offset = byte_str[0] >> 4 # possible value: 14
    next_backward_length = 4 + byte_str[0] - offset * 16
    pointer = 1
    if offset == 15:
        offset += byte_str[1]
        pointer += 1
    valid_bytes = byte_str[pointer:pointer + offset]
    pointer += offset
    total_len = len(byte_str)
    while pointer < total_len:   
        backward_length = next_backward_length
        distance = int.from_bytes(byte_str[pointer:pointer + 2], 'little')
        pointer += 2
        if backward_length == 19:
            backward_length += byte_str[pointer]
            pointer += 1
        length_info = byte_str[pointer]
        if length_info < 240: # 0b11110000
            pointer += 1
            forward_length = length_info >> 4
            next_backward_length = length_info - forward_length * 16 + 4
        else:
            forward_length = byte_str[pointer + 1] + 15
            next_backward_length = length_info - (length_info >> 4) * 16 + 4
            pointer += 2
        # print(pointer, forward_length)
        while -1 * distance + backward_length >= 0:
            valid_bytes += valid_bytes[-1 * distance : -1]
            backward_length -= (distance - 1)
        else:
            valid_bytes += valid_bytes[-1 * distance : -1 * distance + backward_length]
        if forward_length > 0:
            valid_bytes += byte_str[pointer: pointer + forward_length]
        pointer += forward_length
        try:
            valid_bytes.decode('utf-8')
        except:
            pdb.set_trace()
    return valid_bytes.decode('utf-8')

if __name__ == '__main__':
    f = open('a2.bin', 'rb')
    st = f.read()
    print(uncompress(st))
