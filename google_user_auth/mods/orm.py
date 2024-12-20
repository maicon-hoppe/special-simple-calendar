from typing import Annotated, Literal

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext as _


class CalendarUserManager(BaseUserManager):
    """
    Gerente de usuarios para APIs do Google
    """

    def create_user(
        self,
        google_id: str,
        access_token: str,
        refresh_token: str,
        expiry: Annotated[str, "ISO fromat"],
        first_name: Literal["user"] | str = "user",
        full_name: Literal["user"] | str = "user",
        profile_picture: Literal["png"] | Annotated[str, "URL"] = "png",
    ) -> AbstractBaseUser:
        from google_user_auth.models import CalendarUser

        new_user = CalendarUser(
            google_id=google_id,
            access_token=access_token,
            refresh_token=refresh_token,
            first_name=first_name,
            full_name=full_name,
            profile_picture=profile_picture,
            expiry=expiry,
        )

        new_user.save()
        return new_user

    def create_superuser(
        self,
        google_id: str,
        access_token: str,
        refresh_token: str,
        password: str,
        expiry: Annotated[str, "ISO format"],
        first_name: Literal["admin"] | str = "admin",
        full_name: Literal["superuser"] | str = "superuser",
        profile_picture: Literal["png"] | Annotated[str, "URL"] = "png",
    ) -> AbstractBaseUser:
        from google_user_auth.models import CalendarUser

        try:
            int(google_id)
        except ValueError:
            new_user = CalendarUser(
                google_id=google_id,
                access_token=access_token,
                refresh_token=refresh_token,
                password=password,
                first_name=first_name,
                full_name=full_name,
                profile_picture=profile_picture,
                expiry=expiry,
                is_staff=True,
                is_superuser=True,
            )

            new_user.set_password(password)
            new_user.save()

            # all_perms = Permission.objects.all()
            # new_user.user_permissions.add(*all_perms)

            return new_user
        else:
            print(_("\033[1;31mSuperuser ID cannot be a number\033[m"))
            raise KeyboardInterrupt
