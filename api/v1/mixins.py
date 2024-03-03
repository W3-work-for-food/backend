from rest_framework import mixins, viewsets


class RetrieveUpdateListMixins(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    pass
