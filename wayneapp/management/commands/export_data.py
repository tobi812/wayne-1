from django.core.management import BaseCommand
from django.core.paginator import Paginator, Page
from wayneapp.constants import CommandsConstants as Constants
from wayneapp.services import BusinessEntityManager, logging, settings, MessagePublisher


class Command(BaseCommand):

    help = 'publish all data from a business entity to the business entity channel/topic'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._chunk_size = settings.DEFAULT_CHUNK_SIZE
        self._message_service = MessagePublisher()

    def add_arguments(self, parser):
        parser.add_argument(Constants.BUSINESS_ENTITY, type=str)
        parser.add_argument(Constants.CHUNK_SIZE, type=int, nargs='?', default=settings.DEFAULT_CHUNK_SIZE)

    def handle(self, *args, **kwargs):
        self._chunk_size = kwargs[Constants.CHUNK_SIZE]
        business_entity = kwargs[Constants.BUSINESS_ENTITY]
        queryset = self._entity_manager.find_all(business_entity)
        for business_entity in queryset.iterator(chunk_size=self._chunk_size):
            self._message_service.send_entity_update_message(business_entity)
        self._message_service.shutdown()
