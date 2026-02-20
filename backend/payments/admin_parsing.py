from .models_parsing import SmsParsingRule
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django import forms

class RegexTestForm(forms.Form):
    test_message = forms.CharField(widget=forms.Textarea, label="Sample SMS")

@admin.register(SmsParsingRule)
class SmsParsingRuleAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'sender_identifier', 'is_active', 'regex_pattern')
    change_form_template = "admin/payments/smsparsingrule/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/test-regex/', self.admin_site.admin_view(self.test_regex_view), name='payments_smsparsingrule_test'),
        ]
        return custom_urls + urls

    def test_regex_view(self, request, object_id):
        rule = self.get_object(request, object_id)
        result = None
        form = RegexTestForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():
            message = form.cleaned_data['test_message']
            result = rule.parse_message(message)
            if not result:
                result = "No Match Found!"

        context = {
            'title': f'Test Regex for {rule.provider_name}',
            'rule': rule,
            'form': form,
            'result': result,
            'opts': self.model._meta,
        }
        return render(request, 'admin/payments/smsparsingrule/test_regex.html', context)
