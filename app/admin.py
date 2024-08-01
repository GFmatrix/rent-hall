from django.contrib import admin
from .models import *
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import redirect

class HallImageInline(admin.TabularInline):
    model = HallImage
    extra = 0

class ApplicationHallImageInline(admin.TabularInline):
    model = Application
    max_num = 0
    fields = ('application_id', 'name', 'created_at',)
    show_change_link = True
    readonly_fields = ('application_id','name','created_at',)
    can_delete = False
    extra = 0

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'id', 'created_at', 'availability', 'application_count',)
    inlines = (HallImageInline, ApplicationHallImageInline, )

    class Media:
        js = ('assets/js/admin.js',)

    def application_count(self, obj):
        return obj.applications.count()
    
    application_count.short_description = 'Arizalar soni'


class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('application_id', 'name', 'director',  'phone_number','email', 'account_number', 'date_from', 'date_to','address', 'created_at', 'hall')
    list_display = ('application_id', 'name', 'formatted_status', 'created_at', 'contract_download', 'accept_reject_button')
    fields = (
        'application_id', 'name', 'director', 'created_at', 'phone_number','email', 'account_number', 'address', 'date_from', 'date_to', 'hall', 'status'
    )
    def formatted_status(self, obj):
        class_map = {
            'review': ['badge text-bg-secondary', 'background-color: #6c757d; color: #fff'],
            'accept': ['badge text-bg-success', 'background-color: #28a745; color: #fff'],
            'reject': ['badge text-bg-danger', 'background-color: #dc3545; color: #fff'],
        }
        class_name = class_map.get(obj.status, '')
        return format_html('<span class="{}" style="{}">{}</span>', class_name[0], class_name[1], obj.get_status_display())
    formatted_status.short_description = 'Status'

    def accept_reject_button(self, obj):
        if obj.status == 'review':
            
            return format_html(
                '<div style="text-align: right;">'
                '<a class="btn btn-success" style="margin-right: 10px;" href="{}">Tasdiqlash</a>'
                '<a class="btn btn-danger" href="{}">Bekor qilish</a>'
                '</div>',
                reverse('admin:accept_application', args=[obj.pk]), 
                reverse('admin:reject_application', args=[obj.pk])
            )
        return ''
    accept_reject_button.short_description = 'Amallar'
    accept_reject_button.allow_tags = True

    def contract_download(self, obj):
        
            
        return format_html(
                '<a class="btn btn-warning" href="{}">'
                '<svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path opacity="0.5" fill-rule="evenodd" clip-rule="evenodd" d="M3 14.25C3.41421 14.25 3.75 14.5858 3.75 15C3.75 16.4354 3.75159 17.4365 3.85315 18.1919C3.9518 18.9257 4.13225 19.3142 4.40901 19.591C4.68577 19.8678 5.07435 20.0482 5.80812 20.1469C6.56347 20.2484 7.56459 20.25 9 20.25H15C16.4354 20.25 17.4365 20.2484 18.1919 20.1469C18.9257 20.0482 19.3142 19.8678 19.591 19.591C19.8678 19.3142 20.0482 18.9257 20.1469 18.1919C20.2484 17.4365 20.25 16.4354 20.25 15C20.25 14.5858 20.5858 14.25 21 14.25C21.4142 14.25 21.75 14.5858 21.75 15V15.0549C21.75 16.4225 21.75 17.5248 21.6335 18.3918C21.5125 19.2919 21.2536 20.0497 20.6517 20.6516C20.0497 21.2536 19.2919 21.5125 18.3918 21.6335C17.5248 21.75 16.4225 21.75 15.0549 21.75H8.94513C7.57754 21.75 6.47522 21.75 5.60825 21.6335C4.70814 21.5125 3.95027 21.2536 3.34835 20.6517C2.74643 20.0497 2.48754 19.2919 2.36652 18.3918C2.24996 17.5248 2.24998 16.4225 2.25 15.0549C2.25 15.0366 2.25 15.0183 2.25 15C2.25 14.5858 2.58579 14.25 3 14.25Z" fill="#000"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M12 16.75C12.2106 16.75 12.4114 16.6615 12.5535 16.5061L16.5535 12.1311C16.833 11.8254 16.8118 11.351 16.5061 11.0715C16.2004 10.792 15.726 10.8132 15.4465 11.1189L12.75 14.0682V3C12.75 2.58579 12.4142 2.25 12 2.25C11.5858 2.25 11.25 2.58579 11.25 3V14.0682L8.55353 11.1189C8.27403 10.8132 7.79963 10.792 7.49393 11.0715C7.18823 11.351 7.16698 11.8254 7.44648 12.1311L11.4465 16.5061C11.5886 16.6615 11.7894 16.75 12 16.75Z" fill="#000"></path> </g></svg>'
                ' Shartnoma </a>',
                reverse('application_file', args=[obj.application_id])
            )
    contract_download.short_description = 'Shartnoma'
    contract_download.allow_tags = True
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('accept/<int:application_id>/', self.admin_site.admin_view(self.accept_application), name='accept_application'),
            path('reject/<int:application_id>/', self.admin_site.admin_view(self.reject_application), name='reject_application'),
        ]
        return custom_urls + urls

    def accept_application(self, request, application_id, *args, **kwargs):
        application = self.get_object(request, application_id)
        application.status = 'accept'
        application.save()
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def reject_application(self, request, application_id, *args, **kwargs):
        application = self.get_object(request, application_id)
        application.status = 'reject'
        application.save()
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def has_add_permission(self, request):
        return False

    class Media:
        css = {
            'all': ('assets/css/admin.css',)
        }

admin.site.register(Application, ApplicationAdmin)
