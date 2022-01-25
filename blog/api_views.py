import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from blog.api.serializers import PostSerializer
from blog.models import Post




@csrf_exempt
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return JsonResponse({"data": PostSerializer(posts, many=True).data})
    elif request.method == "POST":
        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return HttpResponse(
            status=HTTPStatus.CREATED,
            headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        )

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        return JsonResponse(PostSerializer(post).data)
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif request.method == "DELETE":
        post.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])