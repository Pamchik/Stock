from django.contrib import admin
from .models import *


class AssortmentCategoryAdmin(admin.ModelAdmin):
    fields = (("name",),)


class LocationAdmin(admin.ModelAdmin):
    fields = (("name",),)


class AssortmentQualityCategoryAdmin(admin.ModelAdmin):
    fields = (("name",),)


class StockAdmin(admin.ModelAdmin):

    list_display = ("name",)
    list_display_links = ("name",)
    list_filter = ("category", "location")
    search_fields = ("name", "category__name")
    save_on_top = True
    fieldsets = (

        ("General information", {
            # "classes": ("collapse",),
            "fields": (("category",),
                       ("location", "place"),
                       ("name",),
                       ("description",),
                       ("image",)
                       )
        }),
    )


# Register your models here.
admin.site.register(Stock, StockAdmin)
admin.site.register(AssortmentCategory, AssortmentCategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(AssortmentQualityCategory, AssortmentQualityCategoryAdmin)
admin.site.register(Direction)
admin.site.register(Status)
admin.site.register(Transaction)



