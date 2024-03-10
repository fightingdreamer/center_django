from django.db.models import F, ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ParseError, status
from rest_framework.response import Response

from link_shortener import mapping, models, serializers


@api_view(["GET"])
def get_statistics(request, name: str):
    try:
        id_from_name = mapping.decode_drop_padding(name)
    except ValueError:
        return ParseError()
    try:
        redirection = models.Redirection.objects.get(id=id_from_name)
    except ObjectDoesNotExist:
        return NotFound()

    return Response(serializers.StatisticSerializer(redirection).data)


@api_view(["GET"])
def get_user_info(request, name: str):
    try:
        id_from_name = mapping.decode_drop_padding(name)
    except ValueError:
        return ParseError()
    try:
        redirection = models.Redirection.objects.get(id=id_from_name)
    except ObjectDoesNotExist:
        return NotFound()

    return Response(serializers.UserInfoSerializer(redirection).data)


@api_view(["POST"])
def create_redirection(request):
    request_serializer = serializers.LocationSerializer(data=request.data)
    if not request_serializer.is_valid():
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    location = request_serializer.validated_data["location"]

    user_ip = request.META.get("REMOTE_ADDR", "255.255.255.255")
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    redirection, created = models.Redirection.objects.get_or_create(
        location=location,
        defaults=dict(
            hits=0,
            user_ip=user_ip,
            user_agent=user_agent,
        ),
    )
    return Response(
        serializers.RedirectionSerializer(redirection).data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )


@csrf_exempt
def redirect(request, name: str):
    try:
        id_from_name = mapping.decode_drop_padding(name)
    except ValueError:
        return HttpResponseRedirect(redirect_to="/")

    try:
        redirection = models.Redirection.objects.get(id=id_from_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(redirect_to="/")

    redirection.hits = F("hits") + 1
    redirection.save()
    return HttpResponseRedirect(redirect_to=redirection.location)
