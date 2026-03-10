from django.contrib import admin
from .models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'image', 'time_created')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('time_created', 'ticket', 'user')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
