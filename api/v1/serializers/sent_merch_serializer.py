from rest_framework import serializers

from ambassadors.models import SentMerch, Ambassador
from api.v1.serializers import merch_serializer as merch_s
from api.v1.serializers import user_serializer as user_s
from api.v1.serializers import ambassador_serializer as ambassador_s


class SentMerchSerializer(serializers.ModelSerializer):
    """Сериализатор отправки мерча."""
    merch = merch_s.MerchSerializer(many=True)
    sized_merch = serializers.SerializerMethodField()
    ambassador = ambassador_s.AmbassadorReadSerializer()
    user = user_s.UserSerializer()

    class Meta:
        model = SentMerch
        fields = (
            'id', 'user', 'date', 'ambassador', 'merch', 'amount',
            'sized_merch',
        )

    def get_sized_merch(self, obj):
        query = obj.merch.all()
        ambassador = Ambassador.objects.get(id=obj.ambassador.id)
        ambassador_profile = ambassador.profile

        result = []
        for merch in query:
            match merch.category:
                case 'outerwear':
                    sized_merch = (
                        merch.merch_type, ambassador_profile.clothing_size
                    )
                case 'socks':
                    sized_merch = (
                        merch.merch_type, ambassador_profile.foot_size
                    )
                case _:
                    sized_merch = (merch.merch_type, None)
            result.append(sized_merch)
        return result
