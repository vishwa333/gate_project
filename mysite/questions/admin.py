from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('sub_code', 'chap_code', 'chap_name')
    pass
@admin.register(subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('sub_code', 'sub_name')
    pass
@admin.register(question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('q_id', 'q_type','question')
    pass
#admin.site.register(subject)
#admin.site.register(chapter)
admin.site.register(topic)
#admin.site.register(question)
admin.site.register(solution)

