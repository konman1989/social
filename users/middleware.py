from datetime import datetime, timedelta

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from .models import CustomUser


class UpdateUserLastRequest(MiddlewareMixin):
    settings_timedelta = timedelta(seconds=settings.LAST_REQUEST_TIMEDELTA)

    def process_response(self, request, response):
        if request.user.is_authenticated:
            last_request = request.session.get('last_request')

            if last_request is None:
                CustomUser.objects.filter(pk=request.user.pk).update(
                    last_request=now())
                request.session['last_request'] = datetime.now().isoformat()
                return response

            last_request = datetime.strptime(last_request,
                                             '%Y-%m-%dT%H:%M:%S.%f')
            last_request_time_delta = datetime.now() - last_request

            if last_request_time_delta > self.settings_timedelta:
                CustomUser.objects.filter(pk=request.user.pk).update(
                    last_request=now())
                request.session['last_request'] = datetime.now().isoformat()

        return response


