# wechat-text-backup
This project focuses backup wechat messages of windows client.

## Steps
1. Hacking the wechat app password
2. Decrypt the database using `./decrypt`
3. Extract the message using `extract.py`
### Hacking the password
The sqlite databases for wechat windows client are encrypted. You need to hack the database password before you can do anything. The feasible approach is to get the 32 bytes password from the memory directly. To achieve this goal, you probably need to install an old version of wechat, for example 2.6.8.52. Then you need a windows debugger. For example, x64dbg is
an open source alternative. Next you need to attach the debuuger to wechat and search the string reference in
`wechatwin.dll` module; There are two occurrence of the string `DBFactory::encryptDB` and there is one which points to the
instruction region which has `DB cann't be null`. At this region you can find `test edx edx`, which is a few lines lower than
the three `push` instruction lines. Toggle a breakpoint at this instruction and you can find the register `edx` points to a
memory address which holds the 32 bytes password. After obtaining the password you can upgrade
your wechat to a newer version like 2.8.0.112. The password is not changed at least for compatibility.
### Decrypt the database
I finish this step on linux. See [decrypt.md](./decrypt.md) for detail.
## Python tips
Once copied hex string, we can use Python to write to the binary file.
```Python
a = bytes(bytearray.fromhex('A4CB')) # b'\xa4\xcb'
```
## Know issues
Not works well for wechat version >= 2.9 which only allows partial decryption of `Multi/MSG0.db`;

For wechat 2.8.0.112. It is tested that the message can be tracked.

## CompressContent
compressed bytes in LZ4 Block Format

## Extract and Upload
Run `python3 extract.py` and upload output.

```shell
ossutil64 cp -rf read oss://freiwilliger/wechat/
```
## Other solutions
### iphone
Using itune to get the data to pc. Then use [WechatExport-iOS](https://github.com/stomakun/WechatExport-iOS/pull/12) to get the text message. It seems that the sqlite databases are not encrypted. You have Visual Studio on windows to
compile the project. I have tested this method on March 3th, 2021. It works.

It seems that in Chinese market there is service provided by louyue company. It charges the user about 150 RMB to get the message.
### android
Requiring root privilege on android phone.
See [wechat-dump](https://github.com/ppwwyyxx/wechat-dump) for detail.
I do not have root access to my android phone. Therefore, I did not test this
kind of method.