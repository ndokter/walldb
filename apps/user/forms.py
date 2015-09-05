from io import BytesIO

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from PIL import Image

from apps.user.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, label=_('Email'))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            cleaned_data['user'] = authenticate(username=username,
                                                password=password)

        if not cleaned_data.get('user'):
            raise forms.ValidationError(_("Invalid login credentials."))

        return cleaned_data


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification.")
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _("The email address '{}' is already registered".format(email))
            )

        return email.lower()

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError(
                _("The two password fields didn't match.")
            )

    @transaction.atomic
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            UserProfile.objects.create(user=user)

        return user


class ProfileForm(forms.ModelForm):

    def clean_avatar(self):

        def validate_file_size(image_file):
            kilobytes = len(image_file) / 1024

            if kilobytes > settings.MAX_AVATAR_FILE_SIZE:
                raise ValidationError(
                    _('File too large. It must be under 100kb.')
                )

        def validate_file_type(image_file):
            # We need to get a file object for PIL. We might have a path or we
            # might have to read the data into memory.
            if hasattr(image_file, 'temporary_file_path'):
                f = image_file.temporary_file_path()
            elif hasattr(image_file, 'read'):
                f = BytesIO(avatar.read())
            else:
                f = BytesIO(image_file['content'])

            try:
                img = Image.open(f)
            except Exception:
                # Python Imaging Library doesn't recognize it as an image
                raise ValidationError(
                    _('Unsupported image type. Please upload bmp, png or jpeg.')
                )

            if img.format not in ('BMP', 'PNG', 'JPEG'):
                raise ValidationError(
                    _('Unsupported image type. Please upload bmp, png or jpeg.')
                )

        avatar = self.cleaned_data.get('avatar')

        if avatar:
            validate_file_type(avatar)
            validate_file_size(avatar)

        return avatar

    class Meta:
        model = UserProfile
        fields = ('avatar', 'is_public')
