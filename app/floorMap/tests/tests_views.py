# coding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from app.founder.factories import FounderFactory
from app.mentor.factories import MentorFactory
from app.home.factories import StaffUserProfileFactory, \
    ExecutiveUserProfileFactory
from app.company.factories import CompanyStatusFactory


class FloorMapTest (TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'
        self.founder = FounderFactory()
        self.mentor = MentorFactory()
        self.staff = StaffUserProfileFactory()
        self.executive = ExecutiveUserProfileFactory()

        self.status = CompanyStatusFactory()

    def test_room_update(self):
        """
        Tests access to room update form
        """

        """
        Access : Staff
        """
        self.client.logout()
        self.client.login(
            username=self.staff.user.username,
            password="Toto1234!#"
        )

        result = self.client.get(
            reverse('floorMap:room_update'),
            follow=False
        )
        self.assertEqual(result.status_code, 200)

        """
        Access : Founder
        """
        self.client.logout()
        self.client.login(
            username=self.founder.user.username,
            password="Toto1234!#"
        )

        result = self.client.get(
            reverse('floorMap:room_update'),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

        """
        Access : Mentor
        """
        self.client.logout()
        self.client.login(
            username=self.mentor.user.username,
            password="Toto1234!#"
        )

        result = self.client.get(
            reverse('floorMap:room_update'),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

        """
        Access : Executive
        """
        self.client.logout()
        self.client.login(
            username=self.executive.user.username,
            password="Toto1234!#"
        )

        result = self.client.get(
            reverse('floorMap:room_update'),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

        """
        No Access : Not logged
        """
        self.client.logout()

        result = self.client.get(
            reverse(
                'floorMap:room_update', kwargs={
                    'pk': self.founder.userProfile_id
                }),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_floorMap(self):
        """
        To test the display of the floor map.
        """

        """
        Access : Staff
        """
        self.client.logout()
        self.client.login(
            username=self.staff.user.username,
            password="Toto1234!#"
        )

        result = self.client.get(
            reverse('floorMap:index'),
            follow=False
        )
        self.assertEqual(result.status_code, 200)

        """
        Access : Founder
        """
        self.client.logout()
        self.client.login(
            username=self.founder.user.username,
            password="Toto1234!#"
        )

        result = self.client.get(
            reverse('floorMap:index'),
            follow=False
        )
        self.assertEqual(result.status_code, 200)

        """
        Access : Mentor
        """
        self.client.logout()
        self.client.login(
            username=self.mentor.user.username,
            password="Toto1234!#"
        )

        result = self.client.get(
            reverse('floorMap:index'),
            follow=False
        )
        self.assertEqual(result.status_code, 200)

        """
        Access : Executive
        """
        self.client.logout()
        self.client.login(
            username=self.executive.user.username,
            password="Toto1234!#"
        )

        result = self.client.get(
            reverse('floorMap:index'),
            follow=False
        )
        self.assertEqual(result.status_code, 200)

        """
        No Access : Not logged
        """
        self.client.logout()

        result = self.client.get(
            reverse(
                'founder:detail', kwargs={
                    'pk': self.founder.userProfile_id
                }),
            follow=False
        )
        self.assertEqual(result.status_code, 302)
