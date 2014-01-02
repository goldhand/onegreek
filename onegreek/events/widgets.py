from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.safestring import mark_safe

from datetime import date, datetime


DATETIME_INPUT_FORMATS = getattr(settings, 'DATETIME_INPUT_FORMATS', None)
if DATETIME_INPUT_FORMATS:
    DATETIME_INPUT_FORMATS = DATETIME_INPUT_FORMATS[0]


class BootstrapDateTimeInput(forms.DateTimeInput):
    class Media:
        js = (
            settings.STATIC_URL + 'datepicker/js/bootstrap-datetimepicker.min.js',
            settings.STATIC_URL + 'datepicker/js/bootstrap-datetimepicker-init.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'datepicker/css/bootstrap-datetimepicker.min.css',
            )
        }

    def render(self, name, value, attrs=None):
        if value:
            if isinstance(value, date):
                value = datetime(value.year, value.month, value.day)
            if isinstance(value, datetime):
                if DATETIME_INPUT_FORMATS:
                    value = value.strftime(DATETIME_INPUT_FORMATS)
                else:
                    value = value.strftime('%d/%m/%Y %H:%M:%S')
        else:
            value = ''

        output = '''
        <div id="id_%s" class="input-group date" data-bootstrap-widget="datetimepicker">
            <input class="form-control" value="%s" data-format="MM/dd/yyyy hh:mm:ss" name="%s" type="text"></input>
                <span class="add-on">
                  <i data-time-icon="icon-time" data-date-icon="icon-calendar">
                  </i>
                </span>
        </div>
        ''' % (name, value, name)

        return mark_safe(output)
