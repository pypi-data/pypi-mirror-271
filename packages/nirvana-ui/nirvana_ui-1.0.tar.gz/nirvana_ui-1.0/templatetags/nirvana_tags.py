from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def button(label, variant = ""):
    variants = {
        'primary': 'btn btn-primary',
        'secondary': 'btn btn-secondary',
        'danger': 'btn btn-danger',
        'outline' : 'btn btn-outline',
    }

    if( variant == ""):
        class_name = 'btn'
    else:
        class_name = variants.get(variant, 'btn')
        
    button_html = f'<button class="{class_name}">{label}</button>'

    return mark_safe(button_html)
