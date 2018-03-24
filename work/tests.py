from datetime import datetime, timezone, timedelta
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from work.views import ActivityViewSet
from members.models import Member

JST = timezone(timedelta(hours=+9), 'JST')


class ActivityCreateTests(TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.factory = APIRequestFactory()
        self.admin = Member.objects.filter(is_staff=True)[0]
        self.normal = Member.objects.filter(is_staff=False)[0]
        self.view = ActivityViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })

    def create_new_work(self, start_at, end_at=None):
        if end_at:
            request = self.factory.post('/work/', {
                'start_at': start_at.isoformat(),
                'end_at': end_at.isoformat()
            })
        else:
            request = self.factory.post('/work/', {
                'start_at': start_at.isoformat(),
            })
        force_authenticate(request, user=self.admin)
        return self.view(request)

    def get_work(self):
        request = self.factory.get(f'/work/{{id}}/')
        force_authenticate(request, user=self.admin)
        return self.view(request)

    def test_create(self):
        # 1. 12:00 - 12:15
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 12, 0, tzinfo=JST),
            end_at=datetime(2018, 1, 20, 12, 15, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 201)

        # 2. 11:55 - 12:05 (conflict with 1!)
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 11, 55, tzinfo=JST),
            end_at=datetime(2018, 1, 20, 12, 5, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 400)

        # 3. 12:05 - 12:10 (conflict with 1!)
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 12, 5, tzinfo=JST),
            end_at=datetime(2018, 1, 20, 12, 10, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 400)

        # 4. 12:10 - 12:20 (conflict with 1!)
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 12, 10, tzinfo=JST),
            end_at=datetime(2018, 1, 20, 12, 20, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 400)

        # 5. 11:55 - 12:20 (conflict with 1!)
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 11, 55, tzinfo=JST),
            end_at=datetime(2018, 1, 20, 12, 20, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 400)

        # 6. 12:30 - 12:45
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 12, 30, tzinfo=JST),
            end_at=datetime(2018, 1, 20, 12, 45, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 201)

        # 7. 11:55 - 13:00 (conflict with 1 and 6!)
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 11, 55, tzinfo=JST),
            end_at=datetime(2018, 1, 20, 13, 0, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 400)

    def test_incomplete_create(self):
        # 1. 12:00 - 12:15
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 12, 0, tzinfo=JST),
            end_at=datetime(2018, 1, 20, 12, 15, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 201)

        # 2. 11:55 - > (conflict with 1!)
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 11, 55, tzinfo=JST),
        )
        self.assertEqual(response.status_code, 400)

        # 3. 12:10 - > (conflict with 1!)
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 12, 10, tzinfo=JST),
        )
        self.assertEqual(response.status_code, 400)

        # 4. 12:30 - >
        response = self.create_new_work(
            start_at=datetime(2018, 1, 20, 12, 30, tzinfo=JST),
        )
        id_4 = response.data["id"]
        self.assertEqual(response.status_code, 201)

        # 5. 12:45 - > (4 ends at 12:45)
        start_5 = datetime(2018, 1, 20, 12, 45, tzinfo=JST)
        response = self.create_new_work(
            start_at=start_5,
        )
        id_5 = response.data["id"]
        self.assertEqual(response.status_code, 201)
        work = self.get_work().data
        for work in work:
            if work['id'] == id_4:
                self.assertEqual(work['end_at'], start_5.isoformat())

        # 6. 13:00 - 13:15 (5 ends at 13:00)
        start_6 = datetime(2018, 1, 20, 13, 00, tzinfo=JST)
        response = self.create_new_work(
            start_at=start_6,
            end_at=datetime(2018, 1, 20, 13, 15, tzinfo=JST)
        )
        self.assertEqual(response.status_code, 201)
        work = self.get_work().data
        for work in work:
            if work['id'] == id_5:
                self.assertEqual(work['end_at'], start_6.isoformat())
