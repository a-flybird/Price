from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from myapp import views,utils,role_menu,sparepart
app_name = 'api'
urlpatterns = [
#用户相关接口
    url(r'login/', csrf_exempt(views.login_view),),
    url(r'logout/', csrf_exempt(views.logout_view),),
    url(r'register/', csrf_exempt(views.register),),
    url(r'update_user/', csrf_exempt(views.update_user),),
    url(r'show_user/', csrf_exempt(views.show_user),),
    url(r'update_pwd/', csrf_exempt(views.update_pwd),),
    url(r'create_role/', csrf_exempt(role_menu.create_role),),
    url(r'show_role/', csrf_exempt(role_menu.show_role),),
    url(r'show_menus/', csrf_exempt(role_menu.show_menus),),
    url(r'update_role/', csrf_exempt(role_menu.update_role),),
    url(r'show_routers/', csrf_exempt(role_menu.show_routers),),
#RRP数据接口
    url(r'main/', csrf_exempt(views.get_data),),
    url(r'search/', csrf_exempt(views.search),),
    url(r'searchall/', csrf_exempt(utils.searchall),),
    url(r'exportExcel/', csrf_exempt(views.exportExcel),),
    url(r'uploadExcel/', csrf_exempt(views.uploadExcel),),
    url(r'price_list/', csrf_exempt(utils.price_list),),
    url(r'bom_list/', csrf_exempt(utils.bom_list),),
    url(r'upsert_user/', csrf_exempt(utils.upsert_user),),
    url(r'download_user/', csrf_exempt(utils.download_user),),
    url(r'create_item/', csrf_exempt(utils.create_item),),
    url(r'update_item/', csrf_exempt(utils.update_item),name='update_item'),
    url(r'delete_item/', csrf_exempt(utils.delete_item),),
#备件数据接口
    url(r'create_item_bj/', csrf_exempt(sparepart.create_item),),
    url(r'price_list_bj/', csrf_exempt(sparepart.price_list),),
    url(r'update_item_bj/', csrf_exempt(sparepart.update_item),),
    url(r'delete_item_bj/', csrf_exempt(sparepart.delete_item),),
    url(r'download_user_bj/', csrf_exempt(sparepart.download_user),),
    url(r'upsert_user_bj/', csrf_exempt(sparepart.upsert_user),),
    url(r'search_bj/', csrf_exempt(sparepart.search),),
    url(r'exportExcel_bj/', csrf_exempt(sparepart.exportExcel),),
    url(r'uploadExcel_bj/', csrf_exempt(sparepart.uploadExcel),),
    url(r'get_cpq_token/', csrf_exempt(utils.get_cpq_token),),
    url(r'create_price_item/', csrf_exempt(utils.create_price_item),),

    url(r'get_data/', csrf_exempt(views.get_data),),
]

