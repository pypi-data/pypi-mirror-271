# bcmapi

## 说明

集成[编程猫](https://shequ.codemao.cn)的有关用户的API，便捷获取用户信息

## 更新日志

`1.0.0`基础功能

`1.0.1`紧急删除了1.0.0中泄露的cookie

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
