from django.utils.html import format_html


class TagListMixin:
    """
    Mixin para mostrar tags estilizados en modelos de Django Admin.
    """
    tag_field_name = 'tags'  # Nombre del campo ManyToMany con los tags, puede ser sobrescrito

    def tag_list(self, obj):
        """
        Renderiza la lista de tags en el modelo.
        """
        tags = getattr(obj, self.tag_field_name).all()
        rendered_tags = ' '.join([
            format_html(
                '<span class="inline-block text-white px-2 py-0.5 text-xs font-medium rounded-sm" '
                'style="background-color: {};">{}</span>',
                tag.color_code, tag.name
            )
            for tag in tags
        ])
        return format_html(f'<div class="flex flex-wrap gap-1 items-center">{rendered_tags}</div>')

    tag_list.short_description = 'Tags'


__all__ = ('TagListMixin',)
