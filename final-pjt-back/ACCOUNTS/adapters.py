from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountsAdapter(DefaultAccountAdapter):

  def save_user(self, request, user, form, commit=True):
    data = form.cleaned_data
    user = super().save_user(request, user, form, False)
    profile_image = data.get("profile_image")
    region = data.get("region")
    if profile_image:
      user.profile_image = profile_image
    if region:
      user.region = region
    user.save()
    return user