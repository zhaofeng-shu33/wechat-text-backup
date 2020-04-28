# wechat-text-backup
The privilege of wechat is higher on mobile phone than on pc. For example, mobile phone can save many messages but on pc the
message is limited. Text messages are saved in encrypted sqlite database which cannot be decrypted unless you have root access
to your mobile phone. But usually users do not have root access to their mobile phone. Therefore we need to seek a tradeoff between
the two things: tech-hacking and time-saving.

There are some unofficial wechat personal pc client which can act as Wechat PC client but is fexible to save messages in custom
format. The disadvantage is also obvious. You can only save "current" received message. During the time you use the software, you
cannot use your other wechat pc client. But there is an advantage. You can save chat history. Since in official wechat pc client,
you cannot copy the whole chat history (combined). And using some dependent open-source client you can save the xml chat history.

There are also some other solutions which may not be stable. For example, you can use some hook for official wechat pc.
The advantage is that you can work using official wechat pc while saving the received message out of the box. The disadvantage 
is that you can only use specific version of Windows wechat pc client (other OS is not supported, as I have searched GitHub).
Also, the sent message of yourself through PC client is not saved. But there is an advantage. You can enable recent message sync when you approve the logging of PC wechat client on phone. Then you have about recent 20 items of message for recently used channel. The hook problem
gave some API which you can read the database file on PC. But we do not know how this hook work well in the future.

Finally, there are solutions based on hacking wechat windows database password. The basic idea is to get the 32 bytes password from the memory directly. To achieve this goal, you need to install a specific version of wechat, for example 2.6.8.52, which is quite old. Then you need a windows debugger. For example, x64dbg is
an open source alternative. Next you need to attach to wechat using the debugger and search the string reference in
`wechatwin.dll` module; There are two occurrence of the string `DBFactory::encryptDB` and there is one which points to the
instruction region which has `DB cann't be null`. At this region you can find `test edx edx`, which is a few lines lower than
the three `push` instruction lines. Toggle a breakpoint at this instruction and you can find the register `edx` points to a
memory address which holds the 32 bytes password. After obtaining the password you need to upgrade your wechat to newer version. The password is not changed at least for compatibility.

## Python tips
Once copied hex string, we can use Python to write to the binary file.
```Python
a = bytes(bytearray.fromhex('A4CB')) # b'\xa4\xcb'
```
## Know issues
Not works well for wechat version >= 2.9 which only allows partial decryption of `Multi/MSG0.db`;

For wechat 2.8.0.112. It is tested that the message can be tracked.
