
from myapp.token_module import out_token

def judhe_token(request):
    #print(request.headers)
    print(request.META.get('HTTP_AUTHORIZATION'))
    token = request.META.get('HTTP_AUTHORIZATION')
    #name = request.GET.get('username')
    name = 'admin'
    print(name,'+',token)
    token_obj = out_token(name,token)
    if token_obj:
        return True
    else:
        return False
