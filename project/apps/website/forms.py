from django import forms

# from apps.api.models import (
#     Person,
#     Group,
#     Tune,
#     Catalog,
# )

# from django.db import (
#     IntegrityError,
#     transaction,
# )


class LoginForm(forms.Form):

    email = forms.EmailField(
        required=True,
        # label=popover_html(
        #     'Email',
        #     'help-login-email',
        #     'Please enter the email you used when you originally registered for the site.'
        # ),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Email",
                'autofocus': 'autofocus',
            },
        ),
        error_messages={
            'required': 'Please enter your email address.',
        },
    )

    password = forms.CharField(
        required=True,
        # label=popover_html(
        #     'Password',
        #     'help-login-password',
        #     'Please enter the password you used at registration.  If you have forgotten your password please contact support.'
        # ),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Password",
            },
        ),
        error_messages={
            'required': 'Please enter your password.',
        },
    )


# class MergePersonForm(forms.Form):
#     old = forms.CharField(
#         max_length=200,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control input-lg',
#                 'placeholder': 'Person to be Merged',
#             },
#         ),
#     )

#     new = forms.CharField(
#         max_length=200,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control input-lg',
#                 'placeholder': 'Person to Merge Into',
#             },
#         ),
#     )

#     def clean_old(self):
#         data = self.cleaned_data['old']
#         try:
#             Person.objects.get(name=data)
#         except Person.DoesNotExist:
#             raise forms.ValidationError(
#                 u"Old Person does not exist (check spelling and capitalization).".format(data)
#             )
#         return data

#     def clean_new(self):
#         data = self.cleaned_data['new']
#         try:
#             Person.objects.get(name=data)
#         except Person.DoesNotExist:
#             raise forms.ValidationError(
#                 u"New Person does not exist (check spelling and capitalization).".format(data)
#             )
#         return data

#     def clean(self):
#         cleaned_data = super(MergePersonForm, self).clean()
#         old = cleaned_data.get('old')
#         new = cleaned_data.get('new')
#         if old == new:
#             raise forms.ValidationError(
#                 "Old and New can not be the same"
#             )
#         return

#     @transaction.atomic
#     def merge(self):
#         child = Person.objects.get(name=self.cleaned_data['old'])
#         parent = Person.objects.get(name=self.cleaned_data['new'])
#         quartets = child.quartets.all()
#         choruses = child.choruses.all()
#         catalogs = child.catalogs.all()

#         # move related records
#         with transaction.atomic():
#             for quartet in quartets:
#                 quartet.person = parent
#                 try:
#                     quartet.save()
#                 except IntegrityError:
#                     raise forms.ValidationError(
#                         u"There is an existing member for {0} with the name {1}.  Double-check that they are in fact duplicates.  Otherwise, merge manually.".format(quartet, child),
#                     )
#             for chorus in choruses:
#                 chorus.person = parent
#                 try:
#                     chorus.save()
#                 except IntegrityError:
#                     raise forms.ValidationError(
#                         u"There is an existing director for {0} with the name {1}.  Double-check that they are in fact duplicates.  Otherwise, merge manually.".format(chorus, child),
#                     )
#             for catalog in catalogs:
#                 catalog.person = parent
#                 try:
#                     catalog.save()
#                 except IntegrityError:
#                     raise forms.ValidationError(
#                         u"There is an existing catalog for {0}.  Double-check that they are in fact duplicates.  Otherwise, merge manually.".format(catalog),
#                     )
#         # once records are moved, remove redundant group
#         try:
#             child.delete()
#         except Exception as e:
#             raise RuntimeError("Error deleting old person: {0}".format(e))
#         return


# class MergeSongForm(forms.Form):
#     old = forms.CharField(
#         max_length=200,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control input-lg',
#                 'placeholder': 'Song to be Merged',
#             },
#         ),
#     )

#     new = forms.CharField(
#         max_length=200,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control input-lg',
#                 'placeholder': 'Song to Merge Into',
#             },
#         ),
#     )

#     def clean_old(self):
#         data = self.cleaned_data['old']
#         try:
#             Song.objects.get(name=data)
#         except Song.DoesNotExist:
#             raise forms.ValidationError(
#                 u"Old Song does not exist (check spelling and capitalization).".format(data)
#             )
#         return data

#     def clean_new(self):
#         data = self.cleaned_data['new']
#         try:
#             Song.objects.get(name=data)
#         except Song.DoesNotExist:
#             raise forms.ValidationError(
#                 u"New Song does not exist (check spelling and capitalization).".format(data)
#             )
#         return data

#     def clean(self):
#         cleaned_data = super(MergeSongForm, self).clean()
#         old = cleaned_data.get('old')
#         new = cleaned_data.get('new')
#         if old == new:
#             raise forms.ValidationError(
#                 "Old and New can not be the same"
#             )

#     def merge(self):
#         child = Song.objects.get(name=self.cleaned_data['old'])
#         parent = Song.objects.get(name=self.cleaned_data['new'])
#         catalogs = child.catalogs.all()
#         # move related records
#         for catalog in catalogs:
#             catalog.song = parent
#             try:
#                 catalog.save()
#             except IntegrityError:
#                 ps = catalog.performances.all()
#                 for p in ps:
#                     p.catalog = Catalog.objects.get(
#                         song=parent,
#                         person=catalog.person,
#                     )
#                     p.save()
#         # once records are moved, remove redundant object
#         try:
#             child.delete()
#         except Exception as e:
#             raise RuntimeError("Error deleting old song: {0}".format(e))
#         return


# class MergeGroupForm(forms.Form):
#     old = forms.CharField(
#         max_length=200,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control input-lg',
#                 'placeholder': 'Group to be Merged',
#             },
#         ),
#     )

#     new = forms.CharField(
#         max_length=200,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control input-lg',
#                 'placeholder': 'Group to Merge Into',
#             },
#         ),
#     )

#     def clean_old(self):
#         data = self.cleaned_data['old']
#         try:
#             data = Group.objects.get(name=data)
#         except Group.DoesNotExist:
#             raise forms.ValidationError(
#                 u"Old Group does not exist (check spelling and capitalization).".format(data)
#             )
#         return data

#     def clean_new(self):
#         data = self.cleaned_data['new']
#         try:
#             data = Group.objects.get(name=data)
#         except Group.DoesNotExist:
#             raise forms.ValidationError(
#                 u"New Group does not exist (check spelling and capitalization).".format(data)
#             )
#         return data

#     def clean(self):
#         cleaned_data = super(MergeGroupForm, self).clean()
#         old = cleaned_data.get('old')
#         new = cleaned_data.get('new')
#         if old == new:
#             raise forms.ValidationError(
#                 "Old and New can not be the same"
#             )
#         old_obj = Group.objects.get(name=old)
#         new_obj = Group.objects.get(name=new)
#         if old_obj.kind != new_obj.kind:
#             raise forms.ValidationError(
#                 "Can not merge quartets and choruses."
#             )

#     def merge(self):
#         child = Group.objects.get(name=self.cleaned_data['old'])
#         parent = Group.objects.get(name=self.cleaned_data['new'])
#         contestants = child.contestants.all()
#         # move related records
#         with transaction.atomic():
#             for contestant in contestants:
#                 contestant.group = parent
#                 try:
#                     contestant.save()
#                 except IntegrityError:
#                     raise forms.ValidationError(
#                         u"There is a Contest conflict betwen {0} and {1}.  Double-check that they are in fact duplicates.  Otherwise, merge manually.".format(parent, child),
#                     )
#         # once records are moved, remove redundant group
#         try:
#             child.delete()
#         except Exception as e:
#             raise RuntimeError("Error deleting old group: {0}".format(e))
#         return
