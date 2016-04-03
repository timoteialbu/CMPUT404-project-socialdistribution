from django.views.generic import View
from django.http import HttpResponse
from django import get_version
from django.shortcuts import redirect
from django.conf import settings


class Index(View):
	def get(self, request, *args, **kwargs):
		return redirect(settings.PUBLIC_URL)
