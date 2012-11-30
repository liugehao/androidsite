from django.contrib import admin
from androids.models import Archive, Upfile



class UpfileAdmin(admin.ModelAdmin):
    pass

class UpfileInline(admin.TabularInline):
    model = Upfile
    
class ArchiveAdmin(admin.ModelAdmin):
    fields = ['title', 'version', 'androidversion', 'screen', 'author', 'description']
    inlines = [UpfileInline,]
    list_display = ('id', 'title',"category","url" )
    list_filter = ( 'category',)
    search_fields  = ("id","title",)
admin.site.register(Archive, ArchiveAdmin)
admin.site.register(Upfile)

