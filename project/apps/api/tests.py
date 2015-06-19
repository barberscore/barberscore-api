from nose.tools import (
    ok_,
)

from rest_framework.test import (
    # APIRequestFactory,
    APIClient,
)


from apps.api.factories import (
    QuartetFactory,
)

from apps.api.models import (
    Group,
)


def test_quartet():
    quartet = QuartetFactory(
    )

    ok_(
        quartet.name == "The Buffalo Bills",
        "Name should be 'The Buffalo Bills', is {0}".format(quartet.name),
    )

    ok_(
        quartet.kind == Group.QUARTET
    )

    client = APIClient(
    )

    response = client.get('/api/groups/{0}/'.format(quartet.slug))

    ok_(
        response.status_code == 200,
        "result: {0}".format(response.status_code),
    )

    ok_(
        response.data['name'] == 'The Buffalo Bills'
    )
