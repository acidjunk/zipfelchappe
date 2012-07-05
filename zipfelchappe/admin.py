from django.db import models
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from feincms.admin import item_editor

from . import app_settings
from .models import Project, Reward, Payment, Category
from .widgets import AdminImageWidget
from .utils import get_backer_model

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    prepopulated_fields = {
        'slug': ('title',),
    }

class RewardInlineAdmin(admin.StackedInline):
    model = Reward
    extra = 0
    feincms_inline = True
    fieldsets = [
        [None, {
            'fields': [
                'title',
                ('minimum', 'quantity'),
                'description',
            ]
        }]
    ]

class PaymentInlineAdmin(admin.TabularInline):
    model = Payment
    extra = 0
    raw_id_fields = ('backer','project')
    feincms_inline = True
    #can_delete = False
    #readonly_fields = ('user', 'amount', 'reward', 'anonymously')

    #def has_add_permission(self, request):
    #    return False


class DefaultBackerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    raw_id_fields = ['user']
    inlines = [PaymentInlineAdmin]

class ProjectAdmin(item_editor.ItemEditor):
    inlines = [RewardInlineAdmin, PaymentInlineAdmin]
    date_hierarchy = 'end'
    list_display = ['title', 'goal']
    search_fields = ['title', 'slug']
    readonly_fields = ('achieved_pretty',)
    raw_id_fields = ('author',)
    filter_horizontal = ['categories']
    prepopulated_fields = {
        'slug': ('title',),
        }

    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

    fieldset_insertion_index = 1
    fieldsets = [
        [None, {
            'fields': [
                ('title', 'slug'),
                ('goal', 'currency', 'achieved_pretty'),
                ('start', 'end'),
                'author',
            ]
        }],
        [_('teaser'), {
            'fields': [('teaser_image', 'teaser_text')],
            'classes': ['feincms_inline'],
        }],
        [_('categories'), {
            'fields': ['categories'],
            'classes': ['feincms_inline'],
        }],
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    def achieved_pretty(self, p):
        if p.id:
            return u'%d %s (%d%%)' % (p.achieved, p.currency, p.percent)
        else:
            return u'unknown'
    achieved_pretty.short_description = _('achieved')

    class Media:
        css = { "all" : (
            "zipfelchappe/css/project_admin.css",
            "zipfelchappe/css/feincms_extended_inlines.css",
            "zipfelchappe/css/admin_hide_original.css",
        )}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)

if app_settings.BACKER_MODEL == 'zipfelchappe.Backer':
    BackerModel = get_backer_model()
    admin.site.register(BackerModel, DefaultBackerAdmin)
