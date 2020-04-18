# Procedures
```
# create a file called default.pass which is 32 bytes long and contains the password
# the password can
# be obtained from x64dbg or other
# debuggers. Be cautious about the
# Big Eudian problem
g++ decrypt.cpp -lcrypto -o decrypt
# move windows db file to your linux server
decrypt Media.db
# get Media.db.dec.db
# which can be opened by normal sqlite shell
```

Some observations
* The password is not changed on a fixed windows machine
  even when wechat is upgraded
* All database db file use the same password

