from django.views.generic import View
from django.http import HttpResponse
from django import get_version
from django.shortcuts import redirect
from django.conf import settings

class Index(View):

    def get(self, request, *args, **kwargs):
	if not request.user.is_authenticated():
		return redirect(settings.LOGIN_URL)
        return HttpResponse('Running Django ' + str(get_version()) + " on OpenShift")
	
