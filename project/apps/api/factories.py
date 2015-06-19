from factory.django import (
    DjangoModelFactory,
)

from factory import (
    SubFactory,
)

from .models import (
    Group,
    District,
)


class DistrictFactory(DjangoModelFactory):
    name = "FWD"
    kind = District.DISTRICT

    class Meta:
        model = District


class QuartetFactory(DjangoModelFactory):
    name = "The Buffalo Bills"
    kind = Group.QUARTET
    district_fk = SubFactory(DistrictFactory)

    class Meta:
        model = Group
