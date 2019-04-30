"""Contains view(sets) for the API."""

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .filters import (
    GameFilter,
    MatchupStatsNodeFilter,
    PlayerFilter,
    PlayerRatingNodeFilter,
    PlayerStatsNodeFilter,
    RatingPeriodFilter,
    UserFilter,
)
from .models import (
    Game,
    MatchupStatsNode,
    Player,
    PlayerRatingNode,
    PlayerStatsNode,
    RatingPeriod,
    User,
)
from .serializers import (
    GameSerializer,
    MatchupStatsNodeSerializer,
    PlayerSerializer,
    PlayerRatingNodeSerializer,
    PlayerStatsNodeSerializer,
    RatingPeriodSerializer,
    UserReadOnlySerializer,
)


@swagger_auto_schema(
    method="get", responses={status.HTTP_200_OK: UserReadOnlySerializer}
)
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def current_user(request, token):
    """Determine the current user by their token, and return their data."""
    try:
        user = Token.objects.get(key=token).user
    except ObjectDoesNotExist:
        return Response(
            {"Bad request": "Token does not correspond to an existing user"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(UserReadOnlySerializer(user).data)


class ObtainAuthTokenView(APIView):
    """Return auth token for passed in user."""

    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer
    queryset = Token.objects.all()

    @swagger_auto_schema(
        request_body=AuthTokenSerializer,
        responses={
            status.HTTP_200_OK: Schema(
                type=TYPE_OBJECT,
                properties={"token": Schema(type=TYPE_STRING)},
            )
        },
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.ge(user=user)
        return Response({"token": token.key})


class UserViewSet(viewsets.ModelViewSet):
    """A viewset for users."""

    queryset = User.objects.all()
    lookup_field = "username"
    http_method_names = ["get"]
    serializer_class = UserReadOnlySerializer
    filter_class = UserFilter


class RatingPeriodViewSet(viewsets.ModelViewSet):
    """A viewset for rating periods."""

    queryset = RatingPeriod.objects.all()
    http_method_names = ["get"]
    serializer_class = RatingPeriodSerializer
    filter_class = RatingPeriodFilter


class PlayerViewSet(viewsets.ModelViewSet):
    """A viewset for players."""

    queryset = Player.objects.all()
    http_method_names = ["get", "post", "patch"]
    serializer_class = PlayerSerializer
    filter_class = PlayerFilter


class PlayerStatsNodeViewSet(viewsets.ModelViewSet):
    """A viewset for player stats nodes."""

    queryset = PlayerStatsNode.objects.all()
    http_method_names = ["get"]
    serializer_class = PlayerStatsNodeSerializer
    filter_class = PlayerStatsNodeFilter


class MatchupStatsNodeViewSet(viewsets.ModelViewSet):
    """A viewset for matchup stats nodes."""

    queryset = MatchupStatsNode.objects.all()
    http_method_names = ["get"]
    serializer_class = MatchupStatsNodeSerializer
    filter_class = MatchupStatsNodeFilter


class PlayerRatingNodeViewSet(viewsets.ModelViewSet):
    """A viewset for player rating nodes."""

    queryset = PlayerRatingNode.objects.all()
    http_method_names = ["get"]
    serializer_class = PlayerRatingNodeSerializer
    filter_class = PlayerRatingNodeFilter


class GameViewSet(viewsets.ModelViewSet):
    """A viewset for games."""

    queryset = Game.objects.all()
    http_method_names = ["get", "post"]
    serializer_class = GameSerializer
    filter_class = GameFilter

    def get_serializer(self, *args, **kwargs):
        """Inject the user into the serializer if logged in."""
        serializer = super().get_serializer(*args, **kwargs)

        if (
            hasattr(serializer, "fields")
            and self.request.user.is_authenticated
        ):
            serializer.fields[
                "submitted_by"
            ].initial = self.request.user.username

        return serializer
