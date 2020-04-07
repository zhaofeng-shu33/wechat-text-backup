# Procedures
```
mv password-sample.h password.h
# add modify the password, which can
# be obtained from OllyDBG or other
# debuggers. Be cautious about the
# Big Eudian problem
g++ decrypt.cpp -lcrypto -o decrypt
# move windows db file to your linux server
decrypt Media.db
# get dec_Media.db
# which can be opened by normal sqlite shell
```

Some observations
* The password is not changed on a fixed windows machine
  even when wechat is upgraded
* All database db file use the same password

