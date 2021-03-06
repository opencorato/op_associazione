from django.contrib import admin
from op_associazione.models import Membership, Associate, Citizen, Organization, Politician


#override of the InlineModelAdmin to support the link in the tabular inline
class TabularLinkedInline(admin.options.InlineModelAdmin):
    template = "admin/edit_inline/tabular_linked.html"
    admin_model_path = None

    def __init__(self, *args):
        super(TabularLinkedInline, self).__init__(*args)
        if self.admin_model_path is None:
            self.admin_model_path = self.model.__name__.lower()



class MembershipInline(TabularLinkedInline):
    fields = ['associate', 'type_of_membership', 'fee', 'payed', 'payed_at', 'expire_at', 'sent_card_at', 'is_active',  'public_subscription', 'created_at', 'updated_at']
    readonly_fields = ['associate', 'type_of_membership', 'created_at', 'updated_at']
    model = Membership
    extra = 0


class MembershipAdmin(admin.ModelAdmin):
    fields = ['associate','associate_email', 'type_of_membership', 'fee', 'payed', 'payed_at', 'expire_at', 'sent_card_at',
              'is_active', 'notes', 'public_subscription', 'created_at', 'updated_at',]
    readonly_fields = ['associate','associate_email', 'type_of_membership', 'created_at', 'updated_at']
    search_fields = ('associate__last_name', 'associate__first_name', 'associate__email')
    list_filter = ('is_active', 'expire_at', 'payed_at')
    list_display = ('associate', 'associate_email', 'fee', 'payed', 'payed_at', 'expire_at', 'is_active', 'associate_has_subscribed')
    list_per_page = 500
    ordering = ['expire_at']


    def bulk_deactivate(self, request, queryset):
        for obj in queryset:
            obj.deactivate_and_notify()
    bulk_deactivate.short_description = "Disattiva e invia richiesta rinnovo via email"

    def bulk_activate(self, request, queryset):
        for obj in queryset:
            obj.activate_and_notify()
    bulk_activate.short_description = "Attiva velocamente"
    
    actions = [bulk_activate, bulk_deactivate]



class AssociateAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']
    list_display = ('__unicode__', 'created_at', 'last_membership')
    inlines = [MembershipInline,]
    search_fields = ('first_name', 'last_name', 'email' )
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'birth_date', 'gender', 'created_at')
        }),
        ('Contatti', {
            'classes': ('collapse',),
            'fields': ('phone_number', 'email', 'wants_newsletter')
        }),
        ('Indirizzo', {
            'classes': ('collapse',),
            'fields': ('street', 'civic_nb', 'zip_code', 'location', 'province', 'country')
        }),
        ('Indirizzo di spedizione', {
            'classes': ('collapse',),
            'fields': ('exp_street', 'exp_civic_nb', 'exp_zip_code', 'exp_location', 'exp_province', 'exp_country')
        }),
    )


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Associate, AssociateAdmin)
admin.site.register(Citizen, AssociateAdmin) 
admin.site.register(Organization, AssociateAdmin) 
admin.site.register(Politician, AssociateAdmin) 
