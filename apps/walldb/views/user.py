from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView, UpdateView, FormView, \
    ListView

from apps.user.forms import LoginForm, RegisterForm, ProfileForm
from apps.user.mixins import LoginRequiredMixin, UserMixin


class UserAuthenticationBaseView(FormView):
    form_context_name = None
    template_name = 'walldb/user/authentication.html'

    def get_context_data(self, **kwargs):
        kwargs.update(
            register_form=RegisterForm(),
            login_form=LoginForm(),
        )

        return super(UserAuthenticationBaseView, self).get_context_data(**kwargs)


class UserAuthenticationLoginView(UserAuthenticationBaseView):
    form_class = LoginForm
    success_url = reverse_lazy('walldb:index')

    def get_context_data(self, **kwargs):
        context_data = super(UserAuthenticationLoginView, self)\
            .get_context_data(**kwargs)

        context_data['login_form'] = context_data['form']

        return context_data

    def form_valid(self, form):
        auth.login(self.request, form.cleaned_data['user'])

        return super(UserAuthenticationLoginView, self).form_valid(form)


class UserAuthenticationRegisterView(UserAuthenticationBaseView):
    form_class = RegisterForm
    success_url = reverse_lazy('walldb:index')

    def get_context_data(self, **kwargs):
        context_data = super(UserAuthenticationRegisterView, self)\
            .get_context_data(**kwargs)

        context_data['register_form'] = context_data['form']

        return context_data

    def form_valid(self, form):
        form.save()

        user = auth.authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        auth.login(self.request, user)

        return super(UserAuthenticationRegisterView, self).form_valid(form)


class UserAuthenticationLogoutView(RedirectView):
    url = reverse_lazy('walldb:index')

    def get(self, request, *args, **kwargs):
        auth.logout(request)

        return super(UserAuthenticationLogoutView, self)\
            .get(request, *args, **kwargs)


class UserEditView(LoginRequiredMixin, UpdateView):
    template_name = 'walldb/user/profile/edit.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('walldb:user:details',
                            kwargs={'id': self.request.user.pk})

    def get_object(self, queryset=None):
        # Assume users have gotten a profile after registering.
        return self.request.user.walldb_profile


class UserDetailView(UserMixin, TemplateView):
    template_name = 'walldb/user/profile/details.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['context_user'] = self.user

        return context


class UserListView(ListView):
    template_name = 'walldb/user/list.html'

    queryset = User.objects\
        .filter(is_active=True,
                walldb_profile__is_public=True)\
        .order_by('date_joined')
