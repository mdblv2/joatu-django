from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

from joatu.models import JoatuUser, JoatuSkill, JoatuLocation


class JoatuLocationAdmin(admin.ModelAdmin):
    pass

class JoatuSkillAdmin(admin.ModelAdmin):
    pass

class JoatuUserAdmin(admin.ModelAdmin):
    pass

class HTMLFlatPageForm(FlatpageForm):

    class Meta:
        model = FlatPage
        widgets = {
            'content' : TinyMCE(
                attrs={'cols':100, 'rows':30},
                mce_attrs={'width':'560px'})
            }

class HTMLFlatPageAdmin(FlatPageAdmin):
    form = HTMLFlatPageForm


admin.site.register(JoatuUser, JoatuUserAdmin)
admin.site.register(JoatuSkill, JoatuSkillAdmin)
admin.site.register(JoatuLocation, JoatuLocationAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, HTMLFlatPageAdmin)

