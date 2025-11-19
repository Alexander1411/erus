from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from .models import Contact, ContactSubmission

# Customize User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        ('Учетные данные', {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Создание пользователя', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

# Customize Group Admin
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

# Register Contact Admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'subject', 'created_at')
    list_filter = ('created_at', 'consent')
    search_fields = ('last_name', 'first_name', 'patronymic', 'email', 'phone', 'subject')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Персональные данные', {
            'fields': ('last_name', 'first_name', 'patronymic')
        }),
        ('Контактная информация', {
            'fields': ('email', 'phone')
        }),
        ('Сообщение', {
            'fields': ('subject', 'message')
        }),
        ('Дополнительная информация', {
            'fields': ('consent', 'created_at')
        }),
    )

    def full_name(self, obj):
        return f'{obj.last_name} {obj.first_name} {obj.patronymic}'.strip()
    full_name.short_description = 'ФИО'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Register ContactSubmission Admin
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'contact_email', 'mobile', 'created_at')
    list_filter = ('created_at', 'pain_level')
    search_fields = ('last_name', 'first_name', 'contact_email', 'mobile')
    readonly_fields = ('created_at',)

# Unregister default User and Group admins
admin.site.unregister(User)
admin.site.unregister(Group)

# Register custom User and Group admins
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

# Customize admin site
admin.site.site_header = 'Эрус Центр лечения боли'
admin.site.site_title = 'Эрус Центр лечения боли - Панель управления'
admin.site.index_title = 'Панель управления' 