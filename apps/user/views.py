import re

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

# Create your views here.

#user/register
from django.urls import reverse

from apps.user.models import User


def register(request):
    '''注册'''
    if request.method == 'GET':
        '''显示注册页面'''
        return render(request,'register.html')
    else:
        #进行注册处理
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            # 邮箱格式不正确
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        # 若用户未勾选同意协议，则返回提示
        if allow != 'on':
            # 协议不同意
            return render(request, 'register.html', {'errmsg': '请首先同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)  # 去数据库中查找是否有相同用户名
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 业务处理：进行用户注册
        # 使用Django用户系统内置的创建user的方法
            user = User.objects.creat_user(username, email, password)
            user.is_active = 0
            user.save()
        # 返回应答-跳转到首页页面
        return redirect(reverse('goods:index'))

def login(request):
    '''登录'''
    #接收数据
    username = request.POST.get('username')
    password = request.POST.get('pwd')

    #校验数据
    if not all([username,password]):
        return render(request,'login.html',{'errmsg':'数据不完整'})

    #业务处理：登录校验
    user = authenticate(username=username, password=password)
    if user is not None:
        #用户存在，且用户名密码正确
        login(request,user)
        return redirect(reverse('goods:index'))
    else:
        #用户名密码错误
        return render(request,'login.html',{'errmsg':'用户名或密码错误'})
    