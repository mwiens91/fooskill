"""Contains API URL definitions."""

from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from .views import (
    current_user,
    ObtainAuthTokenView,
    GameViewSet,
    MatchupStatsNodeViewSet,
    PlayerViewSet,
    PlayerRatingNodeViewSet,
    PlayerStatsNodeViewSet,
    RatingPeriodViewSet,
    UserViewSet,
)


# A router to register Django REST Framework viewsets
class OptionalSlashRouter(DefaultRouter):
    """A router that makes a trailing slash optional

    Thanks to Ryan Allen on StackOverflow.
    """

    def __init__(self):
        """Make trailing slashes optional."""
        super().__init__()
        self.trailing_slash = "/?"


# Register the routes
router = OptionalSlashRouter()
router.register("games", GameViewSet)
router.register("matchupstatsnodes", MatchupStatsNodeViewSet)
router.register("players", PlayerViewSet)
router.register("playerratingnodes", PlayerRatingNodeViewSet)
router.register("playerstatsnodes", PlayerStatsNodeViewSet)
router.register("ratingperiods", RatingPeriodViewSet)
router.register("users", UserViewSet)


# Schema for Swagger API
schema_view = get_schema_view(
    openapi.Info(title="fooskill API", default_version="v1"),
    validators=["flex", "ssv"],
    public=True,
)


app_name = "api"
urlpatterns = [
    path(r"", include(router.urls)),
    path(r"auth/", include("rest_framework.urls")),
    path(r"api-token-obtain/", ObtainAuthTokenView.as_view()),
    path(r"api-token-current-user/<str:token>/", current_user),
    path(
        r"redoc/",
        schema_view.with_ui("redoc", cache_timeout=None),
        name="schema-redoc",
    ),
    path(
        r"swagger/",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^swagger/(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=None),
        name="schema-json",
    ),
]
