# bcmapi

## 作者

![阿兹卡班毕业生](https://camo.githubusercontent.com/6c7f3fa09735e1f0b342a1ed8be26153629beedafce894d425e8b7812103c5e3/68747470733a2f2f6769746875622d726561646d652d73746174732e76657263656c2e6170702f6170693f757365726e616d653d617a6b626279732673686f775f69636f6e733d74727565267468656d653d746f6b796f6e69676874 "阿兹卡班毕业生")

[阿兹卡班毕业生](https://shequ.codemao.cn/user/11952313)

## 说明

集成[编程猫](https://shequ.codemao.cn)的API，用简单的代码，实现编程猫和python连接！

## 更新日志

`1.0.1`md文档更新

`1.0.0`基础功能

## 教程

### 登录

```python

from bcmapi import Account


# 实例化一个用户

user = Account(cookie='your_cookie')



# 获取用户信息

print(user.getnickname())

print(user.getid())

print(user.getusergold())

print(user.getrealname())

print(user.getrealsex())

print(user.getusername())

print(user.getusername())

print(user.getbirthday())

print(user.getdescription())

print(user.getphone())

print(user.getlevel())

```

### 获取其它用户信息

```python

from bcmapi import OtherAccount



# 实例化一个用户

user = OtherAccount(id=123456)



# 获取用户信息

print(user.getid())

print(user.getnickname())

print(user.getavatarurl())

print(user.getdescription())

print(user.getlevel())

print(user.getworkshopname())

print(user.getworkshoplevel())

print(user.getviewtimes())

print(user.getfanstotal())

print(user.getcollectedtotal())

print(user.getcollecttimes())

print(user.getlikedtotal())

print(user.getattentiontotal())

print(user.getdoing())

print(user.getotherinfo('doing'))

```

### 获取其它工作室信息

```python

from bcmapi import OtherWorkShop



# 实例化一个工作室

workshop = OtherWorkShop(id=123456)



# 获取工作室信息

print(workshop.getid())

print(workshop.getname())

print(workshop.getdescription())

print(workshop.getlevel())

print(workshop.getpreviewurl())

print(workshop.getcreatedtime())

print(workshop.getotherinfo('name'))

```

### 更新自己的工作室信息

```python

from bcmapi import WorkShop



# 实例化一个工作室

workshop = WorkShop(cookie='your_cookie')



# 更新工作室信息

print(workshop.update_workshop(123456, name='new_name', preview_url='new_preview_url', description='new_description'))

```
