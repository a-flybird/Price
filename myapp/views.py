import datetime,uuid,pymysql,openpyxl,base64,requests,json
from django.contrib import auth
from django.contrib.auth import logout,login
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, FileResponse
from lxml.doctestcompare import strip
from myapp.models import UserToken,basedata,Role,User,UserRole
def get_token(user_id):
    token = uuid.uuid4().hex
    out_time = datetime.datetime.now() + datetime.timedelta(days=1)
    u_token = UserToken.objects.filter(user_id=user_id).first()
    print(out_time, u_token, user_id)
    if u_token:
        u_token.token = token
        u_token.out_time = out_time
        u_token.save()
    else:
        user_token = UserToken()
        user_token.token = token
        user_token.user_id = user_id
        user_token.out_time = out_time
        user_token.save()
    return token
def token_decorator(func):
    def judge(request,*args,**kwargs):
        try:
            _token = request.META.get('HTTP_AUTHORIZATION')[7:]
            print(_token)
            user_token = UserToken.objects.filter(token=_token).first()
            if user_token:
                print(user_token.user_id)
                if user_token.out_time.timestamp() > datetime.datetime.now().timestamp():
                    print('当前用户有效',request.META.get('REMOTE_ADDR'),request.META.get('SERVER_NAME'))
                else:
                    return HttpResponse(status=403)
            else:
                return HttpResponse(status=403)
            return func(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return HttpResponse(status=401)
    return judge
def login_view(request):
    ret = {'code': 20000, 'msg': None, 'username':None, 'token':None}
    try:
        user = request.POST.get('username',None)
        pwd = base64.b64decode(request.POST.get('password',None))
        obj = auth.authenticate(request,username=user,password=pwd)
        if obj:
            if obj.is_active:
                login(request,obj)
                token = get_token(obj.id)
                ret['msg'] = '账号密码验证成功'
                ret['username'] = user
                ret['token'] = token
                return JsonResponse(ret)
            else:
                return JsonResponse({'code':200,'msg':'账号已被锁定，请联系管理员'})
        else:
            return JsonResponse({'code':403,'msg':'账号不存在或密码错误'})
    except Exception as err:
        print(err)
        return JsonResponse({'code':400,'msg':'验证失败'})
def logout_view(request):
    logout(request)
    print(request)
    try:
        _token = request.META.get('HTTP_AUTHORIZATION')[7:]
        UserToken.objects.filter(token=_token).delete()
        print(_token)
        return JsonResponse({'code':20000,'msg':'注销成功'})
    except Exception as err:
        print(err)
@token_decorator
def register(request):
    try:
        username = request.POST.get('username',None)
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        role_id = int(request.POST.get('roles',7))
        is_active = True if request.POST.get('is_active', False)=='true' else False
        password = make_password(request.POST.get('password', None))
        user = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,is_active=is_active,password=password)
        role_obj = Role.objects.filter(id=role_id).first()
        UserRole.objects.create(user_id=user,role_id=role_obj)
    except Exception as e:
        print(e)
        return JsonResponse({'code':20005,'msg':'注册失败'})
    return JsonResponse({'code':20000,'msg':'注册成功'})
@token_decorator
def update_user(request):
    try:
        id = request.POST.get('id', None)
        username = request.POST.get('username',None)
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        role_id = int(request.POST.get('roles',7))
        is_active = True if request.POST.get('is_active', False)=='true' else False
        exist_user = User.objects.filter(id=id)
        exist_role = UserRole.objects.filter(user_id_id=id).first()
        if exist_user:
            exist_user.update(first_name=first_name,last_name=last_name,email=email,is_active=is_active)
            if exist_role:
                if exist_role.role_id_id == role_id:
                    pass
                elif exist_role.role_id_id != role_id:
                    exist_role.delete()
                    role_obj = Role.objects.filter(id=role_id).first()
                    UserRole.objects.create(user_id=exist_user.first(), role_id=role_obj)
            else:
                role_obj = Role.objects.filter(id=role_id).first()
                UserRole.objects.create(user_id=exist_user.first(), role_id=role_obj)
    except Exception as e:
        print(e)
        return JsonResponse({'code':20005,'msg':'修改失败'})
    return JsonResponse({'code':20000,'msg':'修改成功'})
@token_decorator
def show_user(request):
    db = pymysql.connect(host="127.0.0.1", user="root", password="******************", db="MYDATA", port=3306)
    cur = db.cursor()
    sql = 'select id,username,first_name,last_name,email,is_active,last_login from auth_user'
    cur.execute(sql)
    data = cur.fetchall()
    total = len(data)
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(data, page_size)
    page_num = request.GET.get('page_num', 1)
    print(page_size,page_num,'34343434')
    context = []
    try:
        if paginator.page(page_num):
            page_of_price = paginator.page(page_num)
            context = list(page_of_price)
    except Exception as e:
        print(e)
        page_num = 1
        page_of_price = paginator.page(page_num)
        context = list(page_of_price)
    jsonData = []
    for row in context:
        res = {}
        res['id'] = row[0]
        res['username'] = row[1]
        res['first_name'] = row[2]
        res['last_name'] = row[3]
        res['email'] = row[4]
        role = UserRole.objects.filter(user_id_id=row[0]).first()
        if role:
            role_code = Role.objects.filter(id=role.role_id_id).first().role_code
            role_name = Role.objects.filter(id=role.role_id_id).first().role_name
            res['roles'] = {'role_id':role.role_id_id,'role_code':role_code,'role_name':role_name}
        res['is_active'] = row[5]
        res['last_login'] = row[6].strftime('%Y-%m-%d %H:%M:%S')
        jsonData.append(res)
    return JsonResponse({'rows': jsonData,'page_num':int(page_num),'total':total})
@token_decorator
def update_pwd(request):
    ret = {'code':20000,'msg':'修改成功'}
    ret2 = {'code': 20005, 'msg': '修改失败'}
    try:
        id = request.POST.get('id',None)
        newpwd = request.POST.get('newpwd', None)
        re_newpwd = request.POST.get('re_newpwd', None)
        print(id,newpwd,re_newpwd)
        user = User.objects.filter(id=id).first()
        if newpwd != re_newpwd:
            return JsonResponse(ret2)
        if user:
            user.password = make_password(newpwd)
            user.save()
            return JsonResponse(ret)
    except Exception as e:
        print(e)
        return JsonResponse(ret2)

# @token_decorator
def get_data(request):
    print(request.META.get('HTTP_AUTHORIZATION'))
    return JsonResponse({'code':200,'msg':'请求成功'})
@token_decorator
def search(request):
    db = pymysql.connect(host="127.0.0.1", user="root", password="******************", db="MYDATA", port=3306)
    cur = db.cursor()
    results = []
    jsonData = []
    if request.method == "GET":
        start = request.GET.get("productcode", None)
        page_size = request.GET.get('page_size', 10)
        page_num = request.GET.get('page_num', 1)
        if start is not None and len(str(start))!=0:
            starts = start.split(',')
            for i in starts:
                starts = strip(i)
                print(starts)
                sql = "SELECT id,productcode,name,model,description,product_type,price_source,RRP_USD,RRP_EUR,RRP_GBP,RRP_RMB FROM myapp_basedata WHERE productcode = '" \
                      + starts + "' OR name like '%" + starts + "%'" + " OR model like '%" + starts + "%'"
                try:
                    cur.execute(sql)
                    results = results + list(cur.fetchall())
                    print(results)
                except Exception as e:
                    raise e
            total = len(results)
            paginator = Paginator(results, page_size)
            context = []
            try:
                if paginator.page(page_num):
                    page_of_price = paginator.page(page_num)
                    context = list(page_of_price)
            except Exception as e:
                print(e)
                page_num = 1
                page_of_price = paginator.page(page_num)
                context = list(page_of_price)
            print(context)
            for row in context:
                res = {}
                res['id'] = row[0]
                res['productcode'] = row[1]
                res['name'] = row[2]
                res['model'] = row[3]
                res['description'] = row[4]
                res['product_type'] = row[5]
                if row[6] == 'Pricing':
                    res['price_source'] = '定价'
                elif row[6] == 'Quotation':
                    res['price_source'] = '报价'
                else:
                    res['price_source'] = row[6]
                res['RRP_USD'] = row[7]
                res['RRP_EUR'] = row[8]
                res['RRP_GBP'] = row[9]
                res['RRP_RMB'] = row[10]
                jsonData.append(res)
            print(jsonData)
            return JsonResponse({'rows': jsonData, 'page_num': int(page_num), 'total': total})
        else:
            print('未找到记录')
        return JsonResponse({'rows':jsonData})
@token_decorator
def exportExcel(request):
    file = open('E:/mysite/test1.xlsx', 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="File template.xlsx"'
    return response
@token_decorator
def uploadExcel(request):
    print('123123132')
    uploadedFile = request.FILES.get('file', None)
    print(uploadedFile)
    wb = openpyxl.load_workbook(filename=uploadedFile)
    ws = wb.get_sheet_names()
    ws = wb.get_sheet_by_name(ws[0])
    headers = ['productcode', 'name', 'model', 'description', 'product_type', 'price_source', 'RRP_USD', 'RRP_EUR',
               'RRP_GBP', 'RRP_RMB']
    lists = []
    rows = ws.max_row
    for row in range(2, rows + 1):
        r = {}
        for col in range(1, len(headers) + 1):
            key = headers[col - 1]
            r[key] = ws.cell(row=row, column=col).value
        lists.append(r)
    db = pymysql.connect(host="127.0.0.1", user="root", password="******************", db="MYDATA", port=3306)
    cur = db.cursor()

    wb = openpyxl.Workbook()
    sheel_name = 'test'
    sheet1 = wb.active
    sheet1.title = sheel_name
    row = 2
    ft0 = openpyxl.styles.PatternFill("solid", fgColor="8ac6d1")
    ft1 = openpyxl.styles.PatternFill("solid", fgColor="ffb6b9")
    ft3 = openpyxl.styles.PatternFill("solid", fgColor="fdcb6e")
    ft2 = openpyxl.styles.Font(name='Calibri', size=11)
    # 写入表头
    for i in range(1, 11):
        sheet1.cell(row=1, column=i, value=headers[i - 1]).fill = ft0
    for cell in lists:
        productcode = cell['productcode']
        name = cell['name']
        model = cell['model']
        description = cell['description']
        product_type = cell['product_type']
        price_source = cell['price_source']
        RRP_USD = cell['RRP_USD']
        RRP_EUR = cell['RRP_EUR']
        RRP_GBP = cell['RRP_GBP']
        RRP_RMB = cell['RRP_RMB']
        try:
            all_list = basedata.objects.get(productcode=productcode)
            if all_list:
                sheet1.cell(row=row, column=1, value=all_list.productcode)
                sheet1.cell(row=row, column=2, value=all_list.name)
                sheet1.cell(row=row, column=3, value=all_list.model)
                sheet1.cell(row=row, column=4, value=all_list.description)
                sheet1.cell(row=row, column=5, value=all_list.product_type)
                sheet1.cell(row=row, column=6, value=all_list.price_source)
                if str(RRP_USD) == all_list.RRP_USD:
                    sheet1.cell(row=row, column=7, value=RRP_USD)
                else:
                    sheet1.cell(row=row, column=7, value=all_list.RRP_USD).fill = ft3
                if str(RRP_EUR) == all_list.RRP_EUR:
                    sheet1.cell(row=row, column=8, value=RRP_EUR)
                else:
                    sheet1.cell(row=row, column=8, value=all_list.RRP_EUR).fill = ft3
                if str(RRP_GBP) == all_list.RRP_GBP:
                    sheet1.cell(row=row, column=9, value=RRP_GBP)
                else:
                    sheet1.cell(row=row, column=9, value=all_list.RRP_GBP).fill = ft3
                if str(RRP_RMB) == all_list.RRP_RMB:
                    sheet1.cell(row=row, column=10, value=RRP_RMB)
                else:
                    sheet1.cell(row=row, column=10, value=all_list.RRP_RMB).fill = ft3
        except:
            sheet1.cell(row=row, column=1, value=str(productcode)).fill = ft1
            sheet1.cell(row=row, column=2, value=name).fill = ft1
            sheet1.cell(row=row, column=3, value=model).fill = ft1
            sheet1.cell(row=row, column=4, value=description).fill = ft1
            sheet1.cell(row=row, column=5, value=product_type).fill = ft1
            sheet1.cell(row=row, column=6, value=price_source).fill = ft1
            sheet1.cell(row=row, column=7, value=RRP_USD).fill = ft1
            sheet1.cell(row=row, column=8, value=RRP_EUR).fill = ft1
            sheet1.cell(row=row, column=9, value=RRP_GBP).fill = ft1
            sheet1.cell(row=row, column=10, value=RRP_RMB).fill = ft1
        row = row + 1
    for row in range(1, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            sheet1.cell(row, col).font = ft2
    excel_name = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    wb.save('test.xlsx')
    file = open('test.xlsx','rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream;charset=UTF-8'
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % excel_name
    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response
