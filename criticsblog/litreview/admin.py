from django.contrib import admin
from .models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'image', 'time_created')


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'headline',
        'ticket_id_display',
        'ticket',
        'user',
        'time_created'
    )

    readonly_fields = ('id',)

    def ticket_id_display(self, obj):
        return obj.ticket.id

    ticket_id_display.short_description = "Ticket ID"


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
