dic = {(60, 12): 4, (50, 0):6, (57, 0):4, (65,2):4,
    (138, 1): 6, (8, 0): 5, (30, 1): 4, (13, 5): 5, (12, 1): 9,
    (25, 5): 5, (26, 5): 9, (13, 0): 9, (27, 3): 4, (88, 10): 7,
    (17, 9): 14, (125, 4): 13, (34, 3): 8, (14, 8): 7, (15, 0): 12,
    (19, 1): 5, (87, 4): 5, (141, 5): 8, (12, 2): 9, (193, 1): 6,
    (35,1):5, (72,1): 6, (28, 3): 5}
dic2 = {(58, 240):16, (29, 241):5, (40, 241):5, (101, 241):5, (7,242):5}
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
            if dic2.get(length_info):
                print('use dic2', distance, length_info)
                backward_length = dic2[length_info]
            else:
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
    print(uncompress(st))
