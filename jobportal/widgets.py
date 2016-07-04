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
