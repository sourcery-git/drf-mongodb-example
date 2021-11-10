from rest_framework.serializers import ModelSerializer
from .models import Account, ShortLink


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class ShortLinkSerializer(ModelSerializer):
    class Meta:
        model = ShortLink
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'account': {
                'read_only': True
            }
        }