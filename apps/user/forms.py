from io import BytesIO
import uuid

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.conf import settings
from PIL import Image

from apps.user.models import UserProfile
from apps.wallpaper.helpers.image import create_thumbnail


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

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
            raise forms.ValidationError('Invalid login credentials.')

        return cleaned_data


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text='Enter the same password as above, for verification.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "The email address '{}' is already registered".format(email)
            )

        return email.lower()

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError(
                "The two password fields didn't match."
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
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={'data-max-file-size': settings.MAX_AVATAR_FILE_SIZE}
        )
    )

    def clean_avatar(self):

        avatar = self.cleaned_data.get('avatar')

        # Validate file size.
        kilobytes = len(avatar) / 1024

        if kilobytes > settings.MAX_AVATAR_FILE_SIZE:
            raise ValidationError(
                'File too large. It must be under {}KB.'.format(
                    settings.MAX_AVATAR_FILE_SIZE
                )
            )

        # Validate file extension.
        if hasattr(avatar, 'temporary_file_path'):
            f = avatar.temporary_file_path()
        elif hasattr(avatar, 'read'):
            f = BytesIO(avatar.read())
        else:
            f = BytesIO(avatar['content'])

        try:
            img = Image.open(f)
        except Exception:
            # Python Imaging Library doesn't recognize it as an image
            raise ValidationError(
                'Unsupported image type. Please upload bmp, png or jpeg.'
            )

        if img.format not in ('BMP', 'PNG', 'JPEG'):
            raise ValidationError(
                'Unsupported image type. Please upload bmp, png or jpeg.'
            )

        # Resize avatar with the thumbnail helper. This will crop the avatar to
        # a 1:1 aspect ratio without stretching the image.
        return SimpleUploadedFile(
            name='t_{}.{}'.format(str(uuid.uuid4()), img.format),
            content=create_thumbnail(avatar, img.format.lower(), 200, 200)
        )

    class Meta:
        model = UserProfile
        fields = ('avatar', 'is_public')
