from django.contrib import admin
from library.models import User,Book,BookRequest
from rest_framework.authtoken.models import Token

class BookRequestAdmin(admin.ModelAdmin):
    list_dislpay=('book','id','user','status',)
    list_filter=('status',)
    search_fields=('user__username','book__title',)
    
class BookAdmin(admin.ModelAdmin):
    list_display=('id','title','stock','status',)
    
admin.site.register(User)
admin.site.register(Token)
admin.site.register(Book,BookAdmin)
admin.site.register(BookRequest,BookRequestAdmin)