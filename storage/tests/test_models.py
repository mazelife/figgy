# encoding: utf-8
'''
Copyright (c) 2013 Safari Books Online. All rights reserved.
'''

import uuid

from django.test import TestCase

from storage import models

class TestModels(TestCase):
    def setUp(self):
        self.book = models.Book.objects.create(pk=str(uuid.uuid4()))
        self.edition = models.Edition.objects.create(book=self.book, title="The Title", version="1.0")

    def test_book_have_unicode_method(self):
        '''The Book should have a __unicode__ method.'''
        expected = 'Book {}'.format(self.book.pk)
        self.assertEquals(expected, unicode(self.book))


