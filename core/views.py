from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post
from .paginations import SimpleResultPagination
from .mixins import UltraModelViewSet
from .serializers import PostSerializer


class PostViewSet(UltraModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at',]
    search_fields = ['title', 'content']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated,),
        'destroy': (IsAuthenticated,),
    }
