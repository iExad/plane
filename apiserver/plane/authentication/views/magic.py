# Python imports
from urllib.parse import urlencode, urljoin

# Django imports
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
from django.views import View

# Third party imports
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Module imports
from plane.authentication.adapter.base import AuthenticationException
from plane.authentication.provider.credentials.magic_code import (
    MagicCodeProvider,
)
from plane.authentication.utils.login import user_login
from plane.authentication.utils.redirection_path import get_redirection_path
from plane.authentication.utils.workspace_project_join import (
    process_workspace_project_invitations,
)
from plane.bgtasks.magic_link_code_task import magic_link
from plane.license.models import Instance


class MagicGenerateEndpoint(APIView):

    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        # Check if instance is configured
        instance = Instance.objects.first()
        if instance is None or not instance.is_setup_done:
            return Response(
                {
                    "error_code": "INSTANCE_NOT_CONFIGURED",
                    "error_message": "Instance is not configured",
                }
            )

        origin = request.META.get("HTTP_ORIGIN", "/")
        email = request.data.get("email", False)
        try:
            # Clean up the email
            email = email.strip().lower()
            validate_email(email)
            adapter = MagicCodeProvider(request=request, key=email)
            key, token = adapter.initiate()
            # If the smtp is configured send through here
            magic_link.delay(email, key, token, origin)
            return Response({"key", str(key)}, status=status.HTTP_200_OK)
        except ImproperlyConfigured as e:
            return Response(
                {
                    "error_code": "IMPROPERLY_CONFIGURED",
                    "error_message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except AuthenticationException as e:
            return Response(
                {
                    "error_code": str(e.error_code),
                    "error_message": str(e.error_message),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError:
            return Response(
                {
                    "error_code": "INVALID_EMAIL",
                    "error_message": "Valid email is required for generating a magic code",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class MagicSignInEndpoint(View):

    def post(self, request):
        referer = request.META.get("HTTP_REFERER", "/")
        # set the referer as session to redirect after login
        request.session["referer"] = referer
        code = request.POST.get("code", "").strip()
        email = request.POST.get("email", "").strip().lower()

        if code == "" or email == "":
            url = urljoin(
                referer,
                "?"
                + urlencode(
                    {
                        "error_code": "EMAIL_CODE_REQUIRED",
                        "error_message": "Email and code are required",
                    }
                ),
            )
            return HttpResponseRedirect(url)
        try:
            provider = MagicCodeProvider(
                request=request, key=f"magic_{email}", code=code
            )
            user = provider.authenticate()
            # Login the user and record his device info
            user_login(request=request, user=user)
            # Process workspace and project invitations
            process_workspace_project_invitations(user=user)
            # Get the redirection path
            path = get_redirection_path(user=user)
            # redirect to referer path
            url = urljoin(referer, path)
            return HttpResponseRedirect(url)

        except AuthenticationException as e:
            url = urljoin(
                referer,
                "?"
                + urlencode(
                    {
                        "error_code": str(e.error_code),
                        "error_message": str(e.error_message),
                    }
                ),
            )
            return HttpResponseRedirect(url)