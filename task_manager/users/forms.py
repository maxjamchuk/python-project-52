from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


USERNAME_LABEL = "Имя пользователя"
PWD_LABEL = "Пароль"


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        label="Имя",
        required=True,
    )
    last_name = forms.CharField(
        max_length=150,
        label="Фамилия",
        required=True,
    )
    username = forms.CharField(
        max_length=150,
        label=USERNAME_LABEL,
        required=True,
    )
    password1 = forms.CharField(
        label=PWD_LABEL,
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        max_length=150,
        required=True,
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=150,
        required=True,
    )
    username = forms.CharField(
        label=USERNAME_LABEL,
        max_length=150,
        required=True,
    )
    password1 = forms.CharField(
        label=PWD_LABEL,
        widget=forms.PasswordInput,
        required=False,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if (p1 or p2) and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].\
            widget.attrs["placeholder"] = USERNAME_LABEL
        self.fields["password"].\
            widget.attrs["placeholder"] = PWD_LABEL
