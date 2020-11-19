# -*- coding: utf-8 -*-
# @Author      ：180732677
# @Email       : yinbao.bai@hytera.com
# @Time        ：2020/5/23  13:52
# @ProjectName : mysite
# @FileName    ：role_menu.py
# @Software    ：PyCharm
import traceback

import pymysql,json
from django.http import JsonResponse
from .views import token_decorator

from myapp.models import Role,Menu,RoleMenu,UserRole,UserToken,User

def get_role(user_id):
    u_token = UserRole.objects.filter(user_id=user_id).first()

@token_decorator
def create_role(request):
    ret = {'code': 20000, 'msg': '创建成功'}
    try:
        req = json.loads(request.body)
        role_code = req['role_code']
        role_name = req['role_name']
        description = req['description']
        menus = req['menus']
        if role_code != None and role_name != None and description != None:
            exist_role_code = Role.objects.filter(role_code=role_code)
            if exist_role_code:
                ret['code'] = 20005
                ret['msg'] = '该角色已存在'
                return JsonResponse(ret)
            else:
                role = Role.objects.create(role_code=role_code, role_name=role_name, description=description)
                if len(menus)>0:
                    for item in menus:
                        print(item)
                        menu_code = item['menu_code']
                        ischecked = item['ischecked']
                        if ischecked:
                            menu_obj = Menu.objects.filter(menu_code=menu_code).first()
                            if menu_obj:
                                RoleMenu.objects.create(role_id=role, menu_id=menu_obj)
                            else:
                                ret['code'] = 20005
                                ret['msg'] = '菜单错误'
                return JsonResponse(ret)
        else:
            ret['code'] = 20005
            ret['msg'] = '创建失败'
        return JsonResponse(ret)
    except Exception as e:
        print(e)
        ret['code'] = 20006
        ret['msg'] = '未知异常'
        return JsonResponse(ret)

@token_decorator
def update_role(request):
    ret = {'code': 20000, 'msg': '修改成功'}
    try:
        req = json.loads(request.body)
        role_code = req['role_code']
        role_name = req['role_name']
        description = req['description']
        menus = req['menus']
        print(req)
        if role_code != None and role_name != None and description != None:
            exist_role_code = Role.objects.filter(role_code=role_code)
            if exist_role_code:
                exist_role_code.update(role_name=role_name, description=description)
                role_id = exist_role_code.first()
                if len(menus)>0:
                    for item in menus:
                        print(item)
                        menu_code = item['menu_code']
                        ischecked = item['ischecked']
                        menu_obj = Menu.objects.filter(menu_code=menu_code).first()
                        if ischecked:
                            role_menu_obj = RoleMenu.objects.filter(role_id=role_id,menu_id=menu_obj)
                            if role_menu_obj:
                                continue
                            else:
                                RoleMenu.objects.create(role_id=role_id, menu_id=menu_obj)
                        else:
                            role_menu_obj = RoleMenu.objects.filter(role_id=role_id, menu_id=menu_obj)
                            if role_menu_obj:
                                role_menu_obj.delete()
                            else:
                                continue
                return JsonResponse(ret)
            else:
                ret['code'] = 20005
                ret['msg'] = '该角色不存在'
                return JsonResponse(ret)
        else:
            ret['code'] = 20005
            ret['msg'] = '修改失败'
        return JsonResponse(ret)
    except Exception as e:
        print(e)
        ret['code'] = 20006
        ret['msg'] = '未知异常'
        return JsonResponse(ret)

@token_decorator
def show_role(request):
    db = pymysql.connect(host="127.0.0.1", user="root", password="******************", db="MYDATA", port=3306)
    cur = db.cursor()
    sql = 'select id,role_code,role_name,description,create_time from myapp_role'
    cur.execute(sql)
    data = cur.fetchall()
    jsonData = []
    for row in data:
        res = {}
        res['id'] = row[0]
        res['role_code'] = row[1]
        res['role_name'] = row[2]
        res['description'] = row[3]
        res['create_time'] = row[4]
        jsonMenu = []
        menus = RoleMenu.objects.filter(role_id=row[0])
        if menus:
            for menu in menus:
                menu_id = menu.menu_id_id
                menus_obj = Menu.objects.filter(id=menu_id).first()
                re = {}
                re['id'] = menu_id
                re['menu_code'] = menus_obj.menu_code
                re['menu_name'] = menus_obj.menu_name
                re['description'] = menus_obj.description
                jsonMenu.append(re)
        res['menus'] = jsonMenu
        jsonData.append(res)
    return JsonResponse({'rows': jsonData})

@token_decorator
def show_menus(request):
    db = pymysql.connect(host="127.0.0.1", user="root", password="******************", db="MYDATA", port=3306)
    cur = db.cursor()
    sql = 'select id,menu_code,menu_name,description from myapp_menu'
    cur.execute(sql)
    menus = cur.fetchall()
    jsonData = []
    for menu in menus:
        re = {}
        re['id'] = menu[0]
        re['menu_code'] = menu[1]
        re['menu_name'] = menu[2]
        re['description'] = menu[3]
        jsonData.append(re)
    return JsonResponse({'rows': jsonData})

@token_decorator
def show_routers(request):
    try:
        _token = request.META.get('HTTP_AUTHORIZATION')[7:]
        user_token = UserToken.objects.filter(token=_token).first()
        role = UserRole.objects.filter(user_id_id=user_token.user_id).first()
        res={}
        if role:
            role_obj = Role.objects.filter(id=role.role_id_id).first()
            role_code = role_obj.role_code
            user_obj = User.objects.filter(id=user_token.user_id).first()
            res['user_name'] = user_obj.username
            res['role_code'] = role_code
            menus = RoleMenu.objects.filter(role_id=role.role_id_id)
            jsonMenu=[]
            if menus:
                for menu in menus:
                    menu_id = menu.menu_id_id
                    menus_obj = Menu.objects.filter(id=menu_id).first()
                    re = {}
                    re['name'] = menus_obj.menu_name
                    re['path'] = '/' + menus_obj.menu_code
                    re['component'] = 'Layout'
                    if menus_obj.menu_code == 'loginpage':
                        re['redirect'] = '/loginpage'
                        re['path'] = '/'
                    children = []
                    child = {}
                    child['name'] = menus_obj.menu_name
                    child['path'] = menus_obj.menu_code
                    child['component'] = menus_obj.menu_code
                    child['meta'] = {'icon': menus_obj.icon,'title': menus_obj.menu_name}
                    children.append(child)

                    re['children'] = children
                    jsonMenu.append(re)
            res['routers'] = jsonMenu
        return JsonResponse({'rows': res,'code':20000})
    except Exception as e:
        print(e)
        print(traceback.print_exc())

