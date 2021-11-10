from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Account, ShortLink


class AccountSerializer(DocumentSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}


class ShortLinkSerializer(DocumentSerializer):
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
