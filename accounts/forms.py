# # from django import forms
# # from django.contrib.auth.models import User


# # class UserForm(forms.ModelForm):
# #     class Meta:
# #         model = User
# #         fields = ['email', 'username', 'password']
# #         widgets = {
# #             'email': forms.EmailInput(attrs={'class': 'form-control'}),
# #             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '15자 이내로 입력 가능합니다.'}),
# #             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
# #         }
# #         labels = {
# #             'email': '이메일',
# #             'username': '닉네임',
# #             'password': '비밀번호',
# #         }

# #     def __init__(self, *args, **kwargs):
# #         super(UserForm, self).__init__(*args, **kwargs)
# #         self.fields['username'].widget.attrs['maxlength'] = 15

# from django import forms
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.utils.translation import ugettext_lazy as _

# from .models import User, UserManager


# class UserCreationForm(forms.ModelForm):
#     # 사용자 생성 폼
#     email = forms.EmailField(
#         label=_('Email'),
#         required=True,
#         widget=forms.EmailInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': _('Email address'),
#                 'required': 'True',
#             }
#         )
#     )
#     nickname = forms.CharField(
#         label=_('Nickname'),
#         required=True,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': _('Nickname'),
#                 'required': 'True',
#             }
#         )
#     )
#     password1 = forms.CharField(
#         label=_('Password'),
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': _('Password'),
#                 'required': 'True',
#             }
#         )
#     )
#     password2 = forms.CharField(
#         label=_('Password confirmation'),
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': _('Password confirmation'),
#                 'required': 'True',
#             }
#         )
#     )

#     class Meta:
#         model = User
#         fields = ('email', 'nickname')

#     def clean_password2(self):
#         # 두 비밀번호 입력 일치 확인
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserCreationForm, self).save(commit=False)
#         user.email = UserManager.normalize_email(self.cleaned_data['email'])
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


# class UserChangeForm(forms.ModelForm):
#     # 비밀번호 변경 폼
#     password = ReadOnlyPasswordHashField(
#         label=_('Password')
#     )

#     class Meta:
#         model = User
#         fields = ('email', 'password',
#                   'is_active', 'is_superuser')

#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]
