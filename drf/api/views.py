from rest_framework import generics, mixins, permissions

from django.shortcuts import render
from django.db.models import Q

from .serializers import UserProfileSerializer
from .models import UserProfile

from accounts.drfapi.permissions import IsOwnerOrReadOnly

class ListSearchAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserProfileSerializer


    def get_queryset(self):
        queryset = UserProfile.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            queryset = UserProfile.objects.filter(
                Q(title__icontains=query) | \
                Q(address__icontains=query) | \
                Q(country__icontains=query) | \
                Q(city__icontains=query)
            )
            return queryset
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OthersAPIVIew(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def detail(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
