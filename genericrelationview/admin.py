# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

__author__ = 'lexich'


class GenericAdminMixin(object):
    generic_pairs = (('content_type', 'object_id'),)

    def __init__(self, *args, **kwargs):
        super(GenericAdminMixin, self).__init__(*args, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        save_kwargs = dict(kwargs)
        print('GenericAdminMixin', db_field, request)
        for (content_type, object_id) in self.generic_pairs:
            if db_field.name == content_type:
                return self.formfield_for_content_type(
                    db_field, request, object_id, content_type, **kwargs
                )
            elif db_field.name == object_id:
                return self.formfield_for_object_id(db_field, **kwargs)
        return super(
            GenericAdminMixin, self
        ).formfield_for_dbfield(db_field, request, **save_kwargs)

    def formfield_for_content_type(
        self, db_field, request, object_id, content_type, **kwargs
    ):
        formfield = super(
            GenericAdminMixin, self
        ).formfield_for_foreignkey(db_field, request, **kwargs)
        widget = formfield.widget
        url = reverse('generickey_json')
        widget.attrs.update({
            'onchange': "generic_view_json(this,'{0}','{1}','{2}');".format(
                url, object_id, content_type
            ),
            'class': 'generic_view'
        })
        return formfield

    def formfield_for_object_id(self, db_field, **kwargs):
        return db_field.formfield(**kwargs)

    class Media:
        js = (
            'js/admin/generickey.js',
        )
