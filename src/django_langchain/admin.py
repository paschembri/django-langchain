from django.contrib import admin
from .models import SourceDocument, DocumentChunk


@admin.action(description="Parse and index file")
def parse_and_index(modeladmin, request, queryset):
    for instance in queryset:
        instance.parse_file()


class SourceDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "indexed", "chunks_count"]
    actions = [parse_and_index]

    @admin.display(description="Number of chunks")
    def chunks_count(self, instance):
        return instance.documentchunk_set.count()


class DocumentChunkAdmin(admin.ModelAdmin):
    exclude = ["embedding", "index"]
    search_fields = ["page_content"]

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False

        results = queryset.intersection(self.model.objects.search(search_term))
        return results, False


admin.site.register(SourceDocument, SourceDocumentAdmin)
admin.site.register(DocumentChunk, DocumentChunkAdmin)
