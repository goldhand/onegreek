from __future__ import unicode_literals

from django.shortcuts import redirect
from django.template import RequestContext

from django.conf import settings
from .forms import FormForForm
from .models import Form
from .signals import form_invalid, form_valid

from mezzanine.utils.email import split_addresses, send_mail_template
from mezzanine.utils.views import is_spam


def format_value(value):
    """
    Convert a list into a comma separated string, for displaying
    select multiple values in emails.
    """
    if isinstance(value, list):
        value = ", ".join([v.strip() for v in value])
    return value


def form_processor(request, page):
    """
    Display a built form and handle submission.
    """
    form = FormForForm(page.form, RequestContext(request),
                       request.POST or None, request.FILES or None)
    if form.is_valid():
        url = page.get_absolute_url() + "?sent=1"
        if is_spam(request, form, url):
            return redirect(url)
        entry = form.save()
        subject = page.form.email_subject
        if not subject:
            subject = "%s - %s" % (page.form.title, entry.entry_time)
        fields = [(v.label, format_value(form.cleaned_data[k]))
                  for (k, v) in form.fields.items()]
        context = {
            "fields": fields,
            "message": page.form.email_message,
            "request": request,
        }
        email_from = page.form.email_from or settings.DEFAULT_FROM_EMAIL
        email_to = form.email_to()
        if email_to and page.form.send_email:
            send_mail_template(subject, "email/form_response", email_from,
                               email_to, context, fail_silently=settings.DEBUG)
        headers = None
        if email_to:
            # Add the email entered as a Reply-To header
            headers = {'Reply-To': email_to}
        email_copies = split_addresses(page.form.email_copies)
        if email_copies:
            attachments = []
            for f in form.files.values():
                f.seek(0)
                attachments.append((f.name, f.read()))
            send_mail_template(subject, "email/form_response", email_from,
                               email_copies, context, attachments=attachments,
                               fail_silently=settings.DEBUG, headers=headers)
        form_valid.send(sender=request, form=form, entry=entry)
        return redirect(url)
    form_invalid.send(sender=request, form=form)
    return {"form": form}
