import pymysql,csv
from django.contrib import admin
from django.utils.html import format_html
from myapp.models import basedata, importfile,downloadfile,updatefile,upsertfile
from .utils import import_user, download_user,update_user,upsert_user


class basedataAdmin(admin.ModelAdmin):
    def button(self,obj):
        button_html="""<a class="changelink" href="/admin/myapp/basedata/%s/change/">修改</a>""" %(obj.id)
        return format_html(button_html)
    button.short_description = "修改"
    list_display = ['productcode','name','model','description','product_type','price_source','RRP_USD','RRP_EUR','RRP_GBP','RRP_RMB',
                    'createddate', 'lastmodifieddate','button']
    search_fields = ['productcode', 'name']
    date_hierarchy = 'createddate'

class KNImportFileAdmin(admin.ModelAdmin):
    list_display = ['file','createddate']
    list_filter = ['file',]
    def save_model(self, request, obj, form, change):
        re = super(KNImportFileAdmin,self).save_model(request, obj, form, change)
        import_user(self, request, obj, change)
        return re
    def has_delete_permission(self, request, obj=None):
       return False

class DownloadFileAdmin(admin.ModelAdmin):
    list_display = ['down_file','createddate']
    def add_view(self, request, form_url='', extra_context=None):
        return download_user(self,request,obj=None,change=True)
    def has_delete_permission(self, request, obj=None):
       return False

class UpdateFileAdmin(admin.ModelAdmin):
    list_display = ['update_file','lastmodifieddate']
    def save_model(self, request, obj, form, change):
        re = super(UpdateFileAdmin,self).save_model(request, obj, form, change)
        update_user(self, request, obj, change)
        return re
    def has_delete_permission(self, request, obj=None):
       return False

class UpsertFileAdmin(admin.ModelAdmin):
    list_display = ['filename','upsertdate']
    def save_model(self, request, obj, form, change):
        re = super(UpsertFileAdmin,self).save_model(request,obj,form,change)
        upsert_user(self,request,obj,change)
        return re
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(basedata,basedataAdmin)
admin.site.register(importfile,KNImportFileAdmin)
admin.site.register(downloadfile,DownloadFileAdmin)
admin.site.register(updatefile,UpdateFileAdmin)
admin.site.register(upsertfile,UpsertFileAdmin)