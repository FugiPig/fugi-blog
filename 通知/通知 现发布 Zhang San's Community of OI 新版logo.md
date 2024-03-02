现发布 Zhang San's Community of OI 新版logo:
![](https://cdn.luogu.com.cn/upload/image_hosting/h4u721mz.png)

本logo由[@FugiPig](https://www.luogu.com.cn/user/673533)使用Python的turtle模块绘制,[@wawa123](https://www.luogu.com.cn/user/379261)做了修改,增加了原神元素.

turtle源码如下:
```python
import turtle as t
deg=60
t.hideturtle()
t.pensize(7)
t.fd(200)
t.back(130)
t.pensize(15)
t.left(deg)#Z-start
t.fd(60)
t.left(180-deg)
t.fd(35)
t.back(35)
t.left(deg)
t.fd(120)
t.left(180-deg)
t.fd(35)
t.back(35)
t.left(deg)
t.fd(60)
t.right(deg)#Z-end
t.pensize(7)
t.fd(40)
t.pensize(15)
t.left(deg)#S-start
t.fd(60)
t.right(deg)#high -
t.fd(30)
t.back(30)
t.left(deg)#high / again
t.back(60)
t.right(deg)
t.pensize(7)#middle -
t.fd(40)
t.pensize(15)
t.right(180-deg)#low /
t.fd(60)
t.right(deg)#low -
t.fd(25)#S-end
```
Zhang San's Community of OI

FugiPig

2024.2.5