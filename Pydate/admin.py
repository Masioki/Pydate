from django.contrib import admin

from.models import personality_test_item, personality_test_answer, user_data

admin.site.register(personality_test_item)
admin.site.register(personality_test_answer)
admin.site.register(user_data)