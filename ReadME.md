# 第四次作业说明

## 作者：袁仲贤 1900013105

本次作业支持实时通话，但由于方法比较投机取巧的，所以会大大减慢网页的效率
若老师希望尝试 
1. 可以删除 static/js/chatjs中 5个setInterval函数的注释
2. 注释掉setInterval下一行的函数(也是共5个)
3. 通过chrome和edge同时登入两个不同的帐号
4. finish

解决：后来了解到可以使用 flask中的socket-io 搭配 js中的socket来使用
通过socket-io接收某一个用户的请求，socket-io再向各个用户端发出响应，从而使得可以通过判断使用者id和接收者id来
实现实时通话功能，但由于时间不充足，所以在此项目中暂味实现


登入的帐号老师可自行创建或者使用user_info中的username和password进行登录
注:franky franky为编程时使用的帐号