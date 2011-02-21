from django.test import TestCase
from django.contrib.auth.models import User
from models import Entry

from datetime import datetime

class EntryTestCase(TestCase):
    fixtures = ['entries.json', ]

    def testAbsoluteURL(self):
        """ make sure that get_absolute_url returns the correct url """
        entry = Entry.objects.get(pk=1)
        absolute_url = '/%s/%s/' % (entry.pub_date.strftime('%Y/%m/%d'),
                                    entry.slug)

        self.assertEqual(absolute_url, entry.get_absolute_url())

    def testManagers(self):
        """ test managers are returning correct entries """
        all_entries = Entry.objects.all()
        live_entries = Entry.live.all()

        self.assertEqual(len(all_entries), 2)
        self.assertEqual(len(live_entries), 1)

    def testSave(self):
        """ test that custom save method works correctly """
        user = User(username="jon", email='test@example.co.uk')
        user.save()
        entry = Entry(author=user,
                      title='Test Title',
                      excerpt='an excerpt',
                      body='Test body',
                      pub_date=datetime(2010, 01, 01),
                      slug='Test-Title',
                      enable_comments=True,
                      featured=False,
                      status=Entry.LIVE_STATUS,
                      tags='test tag')
        entry.save()
        
        tags = entry.get_tags()
        # test that html is generated
        self.assertEqual(entry.body_html, '<p>Test body</p>')
        self.assertEqual(entry.excerpt_html, '<p>an excerpt</p>')
        # test that tags are saved correctly
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].name, 'test-tag')

        # double check that the entry is saved as live
        self.assertEqual(len(Entry.live.all()), 2)
