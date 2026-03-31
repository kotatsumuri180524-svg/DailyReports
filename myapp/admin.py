from django.contrib import admin
from django.utils.html import format_html

from .models import Report, ReportAttachment


class ReportAttachmentInline(admin.TabularInline):
    model = ReportAttachment
    extra = 0
    fields = ("file", "uploaded_at")
    readonly_fields = ("uploaded_at",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "created_at",
        "has_image",
        "has_upload_file",
        "attachment_count",
        "content_preview",
    )
    list_display_links = ("id", "title")
    list_filter = ("author", "created_at")
    search_fields = ("title", "content", "author__username")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 20
    readonly_fields = ("created_at", "image_preview")
    fieldsets = (
        ("基本情報", {"fields": ("author", "title", "content")}),
        ("添付データ", {"fields": ("image", "image_preview", "upload_file")}),
        ("記録情報", {"fields": ("created_at",)}),
    )
    inlines = (ReportAttachmentInline,)

    def content_preview(self, obj):
        if not obj.content:
            return "-"
        text = obj.content[:40]
        return f"{text}..." if len(obj.content) > 40 else text

    content_preview.short_description = "内容プレビュー"

    def has_image(self, obj):
        return bool(obj.image)

    has_image.boolean = True
    has_image.short_description = "画像"

    def has_upload_file(self, obj):
        return bool(obj.upload_file)

    has_upload_file.boolean = True
    has_upload_file.short_description = "資料"

    def attachment_count(self, obj):
        return obj.attachments.count()

    attachment_count.short_description = "添付数"

    def image_preview(self, obj):
        if not obj.image:
            return "画像はありません"
        return format_html('<img src="{}" alt="添付画像" style="max-width: 240px;" />', obj.image.url)

    image_preview.short_description = "画像プレビュー"
