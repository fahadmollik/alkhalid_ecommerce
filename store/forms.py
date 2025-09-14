from django import forms
from django.core.validators import RegexValidator
from .models import DeliveryOption

class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'আপনার নাম',
            'required': True
        }),
        error_messages={
            'required': 'দয়া করে আপনার নাম লিখুন।',
            'max_length': 'নাম অবশ্যই ১০০ অক্ষরের কম হতে হবে।'
        }
    )
    
    customer_phone = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^(\+8801|01)[3-9]\d{8}$',
                message='দয়া করে একটি সঠিক বাংলাদেশী ফোন নম্বর দিন (যেমন: 01712345678)'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'আপনার মোবাইল নাম্বার',
            'type': 'tel',
            'required': True
        }),
        error_messages={
            'required': 'দয়া করে আপনার ফোন নম্বর লিখুন।'
        }
    )
    
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'আপনার ইমেইল ঠিকানা'
        }),
        error_messages={
            'invalid': 'দয়া করে একটি সঠিক ইমেইল ঠিকানা লিখুন।'
        }
    )
    
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'আপনার বাসার সম্পূর্ণ ঠিকানা',
            'rows': 4,
            'required': True
        }),
        error_messages={
            'required': 'দয়া করে আপনার ঠিকানা লিখুন।'
        }
    )
    
    delivery_option = forms.ModelChoiceField(
        queryset=DeliveryOption.objects.filter(is_active=True),
        empty_label=None,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        error_messages={
            'required': 'দয়া করে একটি ডেলিভারি অপশন নির্বাচন করুন।',
            'invalid_choice': 'দয়া করে একটি সঠিক ডেলিভারি অপশন নির্বাচন করুন।'
        }
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'ডেলিভারির জন্য কোন বিশেষ নির্দেশাবলী',
            'rows': 3
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set delivery option choices
        delivery_options = DeliveryOption.objects.filter(is_active=True)
        if delivery_options.exists():
            self.fields['delivery_option'].initial = delivery_options.first()
        
        # Add error classes to fields with errors
        if self.is_bound and self.errors:
            for field_name, field in self.fields.items():
                if field_name in self.errors:
                    widget_attrs = field.widget.attrs
                    css_classes = widget_attrs.get('class', '')
                    if 'is-invalid' not in css_classes:
                        widget_attrs['class'] = f"{css_classes} is-invalid".strip()