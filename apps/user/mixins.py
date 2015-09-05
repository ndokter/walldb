from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class UserMixin(object):
    user = None

    def dispatch(self, request, *args, **kwargs):
        """
        Fetches User object based on URL id or session. If the User isnt the
        same as the one logged in (if logged in), then check if the user has
        made its profile public.
        """
        self.user = get_object_or_404(User, id=kwargs.get('id'))

        # If the user being requested isnt the logged in user, then first check
        # if he/she is allowed to see that profile based on that profiles
        # is_public flag.
        if self.user != request.user and not self.user.walldb_profile.is_public:
            return HttpResponseForbidden()

        return super(UserMixin, self).dispatch(request, *args, **kwargs)
