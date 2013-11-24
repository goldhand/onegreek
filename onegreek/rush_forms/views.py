from __future__ import unicode_literals

from django.shortcuts import redirect, get_object_or_404, render
from django.template import RequestContext

from django.conf import settings
from .forms import FormForForm
from .models import Form
from .signals import form_invalid, form_valid

from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, YAMLRenderer

def format_value(value):
    """
    Convert a list into a comma separated string, for displaying
    select multiple values in emails.
    """
    if isinstance(value, list):
        value = ", ".join([v.strip() for v in value])
    return value


def form_view(request, pk):
    """
    Display a built form and handle submission.
    """
    _form = get_object_or_404(Form, pk=pk)
    form = FormForForm(_form, RequestContext(request),
                       request.POST or None, request.FILES or None)
    if form.is_valid():
        url = request.path + "?sent=1"
        entry = form.save()
        form_valid.send(sender=request, form=form, entry=entry)
        return redirect(url)
    form_invalid.send(sender=request, form=form)
    return render(request, "forms/form.html", {"form": form})


@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
@parser_classes((JSONParser, MultiPartParser))
def rush_form_view(request, pk, format=None):
    """
    Display a built form and handle submission.
    """
    rush_form = get_object_or_404(Form, pk=pk)
    print request.POST
    form = FormForForm(rush_form, request.DATA or None, request.FILES or None)
    if form.is_valid():
        entry = form.save()
        entry.user = request.user
        entry.save()
        form_valid.send(sender=request, form=form, entry=entry)
        return Response({'success': True})
    else:
        form_invalid.send(sender=request, form=form)
        return Response({'success': False, 'errors': form.errors, 'data': request.DATA})


'''

def form_view(request, pk):
    """
    Display a built form and handle submission.
    """
    _form = get_object_or_404(Form, pk=pk)
    form = FormForForm(_form, RequestContext(request),
                       request.POST or None, request.FILES or None)
    if form.is_valid():
        url = request.path + "?sent=1"
        entry = form.save()
        #
        ### Commented out because of mezzanine dependencies
        #
        #subject = page.form.email_subject
        #if not subject:
        #    subject = "%s - %s" % (page.form.title, entry.entry_time)
        #fields = [(v.label, format_value(form.cleaned_data[k]))
        #          for (k, v) in form.fields.items()]
        #context = {
        #    "fields": fields,
        #    "message": page.form.email_message,
        #    "request": request,
        #    }
        #email_from = page.form.email_from or settings.DEFAULT_FROM_EMAIL
        #email_to = form.email_to()
        #if email_to and page.form.send_email:
        #    send_mail_template(subject, "email/form_response", email_from,
        #                       email_to, context, fail_silently=settings.DEBUG)
        #headers = None
        #if email_to:
        #    # Add the email entered as a Reply-To header
        #    headers = {'Reply-To': email_to}
        #email_copies = split_addresses(page.form.email_copies)
        #email_copies = []
        #if email_copies:
        #    attachments = []
        #    for f in form.files.values():
        #        f.seek(0)
        #        attachments.append((f.name, f.read()))
        #    send_mail_template(subject, "email/form_response", email_from,
        #                       email_copies, context, attachments=attachments,
        #                       fail_silently=settings.DEBUG, headers=headers)

        form_valid.send(sender=request, form=form, entry=entry)
        return redirect(url)
    form_invalid.send(sender=request, form=form)
    return render(request, "forms/form.html", {"form": form})

'''
