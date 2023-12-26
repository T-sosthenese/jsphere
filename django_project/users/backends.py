"""
Nommarly in django, when the user tries to sign in using
their username, ModelBackend is responsible for looking up for
that username from the backend. This model will enable us to tell
model backend to use the email instead of username for authentication.
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user_query = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username))
            user_ordered = user_query.order_by('id')
            user = user_ordered.first()
        if user.check_password(password) and self.user_can_authenticate(user):
            return user