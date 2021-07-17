# generate a simple index for md files in the folder "reader"
import os
md_str = ""
for i in os.listdir("read"):
    md_str += f'[{i}](read/{i})' + "\n\n"
with open("read_index.md", "wb") as f:
    f.write(md_str.encode('utf-8'))
