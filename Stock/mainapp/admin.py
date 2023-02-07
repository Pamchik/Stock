from django.contrib import admin
from .models import *
from import_export import resources


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
            "fields": (("category",),
                       ("number",),
                       ("name",),
                       ("description",),
                       ("comment",),
                       ("image",)
                       )
        }),
    )


class TestResource(resources.ModelResource):
    class Meta:
        model = Transaction


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(AssortmentCategory, AssortmentCategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(AssortmentQualityCategory, AssortmentQualityCategoryAdmin)
admin.site.register(Direction)
admin.site.register(Status)
admin.site.register(Transaction)
