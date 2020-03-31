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
Also, the sent message of yourself through PC client is not saved. But there is 
