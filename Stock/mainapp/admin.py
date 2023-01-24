from django.contrib import admin
from .models import *
from import_export import resources
from import_export.fields import Field

class AssortmentCategoryAdmin(admin.ModelAdmin):
    fields = (("name",),)


class LocationAdmin(admin.ModelAdmin):
    fields = (("name",),)


class AssortmentQualityCategoryAdmin(admin.ModelAdmin):
    fields = (("name",),)


class ProductAdmin(admin.ModelAdmin):

    list_display = ("name",)
    list_display_links = ("name",)
    list_filter = ("category",)
    search_fields = ("name", "category__name")
    save_on_top = True
    fieldsets = (

        ("General information", {
            # "classes": ("collapse",),
            "fields": (("category",),
                       ("name",),
                       ("description",),
                       ("comment",),
                       ("image",)
                       )
        }),
    )


class TestResource(resources.ModulResorce):
    is_active = Field()
    created = Field()
    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'is_active', 'created')
        export_order = ('id', 'title', 'description', 'is_active', 'created')

    def dehydrate_is_active(self, obj):
        if obj.is_active:
            return "yes"
        return "no"

    def dehydrate_created(self, obj):
        return obj.created.strftime('%d-%m-%Y %H:%M:%S')



# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(AssortmentCategory, AssortmentCategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(AssortmentQualityCategory, AssortmentQualityCategoryAdmin)
admin.site.register(Direction)
admin.site.register(Status)
admin.site.register(Transaction)
admin.site.register(Test)



