from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins

from main.filters import TitleFilter
from main.models import Category, Genre, Title, Review
from main.permissions import IsAdminOrReadOnly, IsAuthorOrModeratorOrReadOnly
from main.serializers import CategorySerializer, GenreSerializer, \
    TitleSerializerPOST, ReviewSerializer, TitleSerializerGET, \
    CommentSerializer


class GetCreateDeleteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                             mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class CategoryViewSet(GetCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(GetCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    http_method_names = ['get', 'post', 'delete', 'patch']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGET
        return TitleSerializerPOST


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        serializer.save(review=review)
