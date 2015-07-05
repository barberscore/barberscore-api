from factory.django import (
    DjangoModelFactory,
)

from .models import (
    Group,
)


class QuartetFactory(DjangoModelFactory):
    name = "The Buffalo Bills"
    kind = Group.QUARTET

    class Meta:
        model = Group
