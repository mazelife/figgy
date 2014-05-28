# encoding: utf-8

from django.db import models


class BaseModel(models.Model):
    '''Base class for all models'''
    created_time = models.DateTimeField('date created', auto_now_add=True)
    last_modified_time = models.DateTimeField('last-modified', auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Book(BaseModel):
    '''
    Main storage for a Book object.
    '''

    id = models.CharField(max_length=30, primary_key=True, help_text="The primary identifier of this title, we get this value from publishers.")

    def __unicode__(self):
        return "Book {}".format(self.pk)

    @property
    def latest_edition(self):
        return self.edition_set.first()

    @property
    def title(self):
        return self.latest_edition.title


class Edition(BaseModel):
    '''
    The edition of a particular book. Title and description vary across editions.
    '''
    book = models.ForeignKey("storage.Book")
    version = models.DecimalField(max_digits=4, decimal_places=1, help_text="The version of the book.", db_index=True)
    title = models.CharField(max_length=128, help_text="The title of this book.", db_index=True, null=False, blank=False)
    description = models.TextField(blank=True, null=True, default=None, help_text="Very short description of this book.")

    class Meta:
        ordering = ("book", "-version")
        unique_together = (("book", "version"),)

    def __unicode__(self):
        return self.title


class Alias(BaseModel):
    '''
    A book can have one or more aliases which...?

    For example, a book can be referred to with an ISBN-10 (older, deprecated scheme), ISBN-13 (newer scheme),
    or any number of other aliases.
    '''

    book = models.ForeignKey(Book, related_name='aliases')
    value = models.CharField(max_length=255, db_index=True, unique=True, help_text="The value of this identifier")
    scheme = models.CharField(max_length=40, help_text="The scheme of identifier")

    def __unicode__(self):
        return '%s identifier for %s' % (self.scheme, self.book.title)
