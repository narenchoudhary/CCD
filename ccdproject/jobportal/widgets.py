from django.forms import CheckboxInput, SelectMultiple
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django import forms


class CheckBoxBootstrapSwitch(forms.CheckboxInput):
    """Django widget for bootstrap switch HTML widget: http://www.bootstrap-switch.org/
    Options can be provided through 'switch' argument:
        switch = forms.BooleanField(required=False, label=_(u"bootstrap switch"),
                widget=CheckBoxBootstrapSwitch(switch={'size': 'small', 'on': 'warning', 'text-label': 'Switch Me'}))
    """
    def __init__(self, switch=None, *args, **kwargs):
        self.switch = switch or {}
        super(CheckBoxBootstrapSwitch, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        checkbox = super(CheckBoxBootstrapSwitch, self).render(name=name, value=value, attrs=attrs)
        data = ''
        size = self.switch.get('size', 'large')  # 'mini', 'small', 'large' or '' for normal
        # handling of data-properties
        for key in ['on', 'off', 'on-label', 'off-label', 'text-label']:
            data += ' data-%s="%s"' % (key, self.switch[key]) if key in self.switch else ''

        widget = '<div id="switch-%s" class="make-switch' % name
        widget += ' switch-' + size if size else ''
        widget += '"' + data + '>' + checkbox
        widget += '</div>'
        widget += '<script>$(document).ready(function () {$("[name=%s]").bootstrapSwitch();});</script>' %name
        print widget
        return widget


class TableSelectMultiple(SelectMultiple):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.

    When providing choices for this field, give the item as the second
    item in all choice tuples. For example, where you might have
    previously used::

        field.choices = [(item.id, item.name) for item in item_list]

    ...you should use::

        field.choices = [(item.id, item) for item in item_list]
    """
    def __init__(self, item_attrs, *args, **kwargs):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callables in item_attrs will be called with the item to be
            displayed as the sole parameter.

            Any callable attribute names specified will be called and have
            their return value used for display.

            All attribute values will be escaped.
        """
        super(TableSelectMultiple, self).__init__(*args, **kwargs)
        self.item_attrs = item_attrs

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = []
        str_values = set([force_unicode(v) for v in value]) # Normalize to strings.
        for i, (option_value, item) in enumerate(self.choices):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            output.append(u'<tr><td>%s</td>' % rendered_cb)
            for attr in self.item_attrs:
                if callable(attr):
                    content = attr(item)
                elif callable(getattr(item, attr)):
                    content = getattr(item, attr)()
                else:
                    content = getattr(item, attr)
                output.append(u'<td>%s</td>' % escape(content))
            output.append(u'</tr>')
        return mark_safe(u'\n'.join(output))