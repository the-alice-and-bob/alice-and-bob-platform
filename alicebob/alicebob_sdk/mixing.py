from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.utils.html import format_html, format_html_join
from unfold.decorators import display


class TagListMixin:
    """
    Mixin para mostrar tags estilizados en modelos de Django Admin.
    """
    tag_field_name = 'tags'  # Nombre del campo ManyToMany con los tags, puede ser sobrescrito
    tag_model = None  # Modelo de los tags, debe ser sobrescrito

    @display(description='Tags')
    def tag_list(self, obj):
        """
        Renderiza la lista de tags en el modelo.
        """
        tags = obj.tags.all()

        # Construye cada etiqueta usando format_html para cada elemento individualmente
        rendered_tags = format_html_join(
            '',  # Sin separador
            '<span class="inline-block text-white px-2 py-0.5 text-xs font-medium rounded-sm" style="background-color: {};">{}</span>',
            [(tag.color_code, tag.name) for tag in tags]  # Pasar valores como una tupla
        )

        # Retorna el contenedor de todas las etiquetas renderizadas
        return format_html(
            '<div class="flex flex-wrap gap-1 items-center">{}</div>', rendered_tags
        )

    def tags_queryset(self, query):
        """
        Sobrescribe el queryset para incluir los tags.
        """
        query = query.prefetch_related('tags')

        query = query.annotate(
            tag_list=ArrayAgg(
                Concat(
                    F('tags__name'),  # Campo con el nombre del tag
                    Value(':'),  # Separador
                    F('tags__color_code'),  # Campo con el código de color
                    output_field=models.CharField()  # Campo de salida
                ),
                distinct=True  # Elimina duplicados si hay redundancias
            )
        )

        return query


__all__ = ('TagListMixin',)
