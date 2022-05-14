from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Review, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('content', 'is_approved')
    search_fields = ('content',)
    actions = ['approve_reviews']

    
    @admin.action(description='Approve Reviews')
    def approve_reviews(self, request, queryset):
        for review in queryset:
            review.is_approved = True
            review.save()
        count = len(queryset)
        self.message_user(request, ngettext(
            '%d review was approved successfully.',
            '%d reviews were approved successfully.',
            count ) % count, messages.SUCCESS)




admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
