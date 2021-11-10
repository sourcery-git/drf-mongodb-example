from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Account, ShortLink
from .serializers import AccountSerializer, ShortLinkSerializer


class AccountViewSet(ModelViewSet):
    ''' ViewSet to manage accounts. '''
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class ShortLinkViewSet(ModelViewSet):
    ''' ViewSet to manage short links under an account. '''
    serializer_class = ShortLinkSerializer

    def look_up_account(self):
        # Check account pk in kwargs before looking it up
        # so that swagger view calls don't throw errors
        if account_pk := self.kwargs.get('account_pk'):
            return get_object_or_404(Account, pk=account_pk)

        # Real calls cannot be made without account PK in the URL
        # so returning None here is safe
        return None

    def get_queryset(self):
        return ShortLink.objects.filter(account=self.look_up_account())

    def perform_create(self, serializer):
        account = self.look_up_account()  # 404 if no account
        # Set short link owner in the `validated_data`
        serializer.validated_data['account'] = account
        super().perform_create(serializer)