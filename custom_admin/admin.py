from django.contrib import admin
from store.models import SiteSettings

class SiteSettingsAdmin(admin.ModelAdmin):
	list_display = ('site_name', 'site_tagline', 'phone_number', 'email', 'facebook_url', 'youtube_url')
	fields = (
		'site_name', 'site_tagline', 'logo', 'favicon',
		'header_bg_color', 'header_text_color',
		'phone_number', 'email', 'address',
		'facebook_url', 'youtube_url',
		'meta_description', 'meta_keywords'
	)

admin.site.register(SiteSettings, SiteSettingsAdmin)
