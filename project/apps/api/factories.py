from factory.django import (
    DjangoModelFactory,
)

from .models import (
    Group,
    District,
)


class QuartetFactory(DjangoModelFactory):
    name = "The Buffalo Bills"
    district = District.FWD
    kind = Group.QUARTET

    class Meta:
        model = Group
