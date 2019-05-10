

# Third-Party
from factory import SubFactory
from factory.django import DjangoModelFactory

# First-Party
from .models import Grid
from .models import Venue


class GridFactory(DjangoModelFactory):
    status = Grid.STATUS.new
    round = SubFactory('api.factories.RoundFactory')

    class Meta:
        model = Grid


class VenueFactory(DjangoModelFactory):
    name = 'Test Convention Center'
    status = Venue.STATUS.active
    city = 'Nashville'
    state = 'TN'
    airport = 'NTA'
    timezone = 'US/Central'

    class Meta:
        model = Venue
