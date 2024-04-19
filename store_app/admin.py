from django.contrib import admin
from .models import *

class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('id' ,'title', 'customizable', 'ecommerce', 'barber', 'created_at')
    list_filter = ('customizable', 'ecommerce', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('image', 'title', 'description', 'html_content', 'html_content1', 'html_content2', 'html_content3')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('css_cotent', 'js_content', 'ecommerce', 'barber', 'customizable', 'template_type')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class UserTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'time_since_updated')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'template')
        }),
        ('Template Data', {
            'fields': ('image', 'title', 'description', 'html_content', 'html_content1', 'html_content2', 'html_content3', 'css_cotent', 'js_content', 'ecommerce', 'barber')
        }),
        ('Additional Information', {
            'fields': ('font_type', 'font_family', 'color_theme_pr', 'color_theme_sc', 'business_name', 'business_logo', 'additional_field'),
            'classes': ('collapse',),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'user_template', 'replied', 'created_at')
    list_filter = ('user_template', 'replied', 'created_at')
    search_fields = ('name', 'email', 'message', 'user_template__title')
    readonly_fields = ('created_at',)
    
class QrCodeHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'url', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__name', 'name', 'url')
    readonly_fields = ('created_at',)
    
class GetStartedAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'template_type', 'font_type', 'color_theme_pr', 'color_theme_sc', 'created_at', 'updated_at')
    list_filter = ('template_type', 'font_type', 'created_at', 'updated_at')
    search_fields = ('business_name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
class AppointmentAdmin(admin.ModelAdmin):  
    list_display = ('user_template', 'name', 'email', 'date', 'time', 'time_since_updated')
    
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_template', 'name', 'email', 'date', 'time', 'time_since_updated')

class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('user_template', 'date', 'time')
class DomainAdmin(admin.ModelAdmin):
    list_display = ('user_template', 'slug', 'custom_domain', 'created_at')
    
    
admin.site.register(Templates, TemplatesAdmin)
admin.site.register(UserTemplate, UserTemplateAdmin)
admin.site.register(QrCodeHistory, QrCodeHistoryAdmin)
admin.site.register(GetStarted, GetStartedAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(AvailableTime, AvailableTimeAdmin)
admin.site.register(Domain, DomainAdmin)