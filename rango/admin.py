from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile
from rango.models import Submission, Feedback, CPU, CPU_Family\

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'title', 'content', 'result', 'owner_id')


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
