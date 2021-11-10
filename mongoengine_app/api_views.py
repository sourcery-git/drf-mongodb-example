from rest_framework_mongoengine.generics import get_object_or_404
from rest_framework_mongoengine.viewsets import ModelViewSet
from .models import Account, ShortLink
from .serializers import AccountSerializer, ShortLinkSerializer


class AccountViewSet(ModelViewSet):
    ''' ViewSet to manage accounts. '''
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class AccountShortLinkViewSet(ModelViewSet):
    ''' ViewSet to manage short links under an account. '''
    serializer_class = ShortLinkSerializer

    def look_up_account(self):
        # Check account pk in kwargs before looking it up
        # so that swagger view calls don't throw errors.
        # NOTE: using `account_id` instead of `account_pk` here
        # because of how rest_framework_mongoengine handles routes
        if account_pk := self.kwargs.get('account_id'):
            # NOTE: passsing `Account.objects` here because the overridden
            # get_object_or_404 accepts a queryset instead of model
            result = get_object_or_404(Account.objects, pk=account_pk)
            return result

        # Real calls cannot be made without account PK in the URL
        # so returning None here is safe
        return None

    def get_queryset(self):
        return ShortLink.objects(account=self.look_up_account())

    def perform_create(self, serializer):
        account = self.look_up_account()
        serializer.validated_data['account'] = account
        super().perform_create(serializer)