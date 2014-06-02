# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 4:58 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.

from decimal import Decimal, InvalidOperation

from storage.models import Alias, Book, Edition
from storage.exceptions import BadDataFile


def process_book_element(book_element):
    """
    Process a book element into the database. Operates on the following assumptions:

    1. A book ID may have a bad value, but if any of it's aliases match a single existing book then an update
    operation on that book can be done safely using the data in the <book> element.
    2. For any given <book> element, if the aliases match more than one book, then one or more of them are incorrect and
    an exception should be raised.
    3. If the book is missing a <version> or if it's not number, an exception should be raised.


    :param book: book element
    :returns:
    :raises: BadDataFile
    """
    book_id = book_element.get('id')
    aliases = [(a.get('scheme'), a.get('value')) for a in book_element.xpath('aliases/alias')]
    edition_version = book_element.findtext('version')
    try:
        edition_version = Decimal(edition_version)
    except InvalidOperation:
        raise BadDataFile("Invalid version data: {} is not a decimal number.".format(edition_version))
    except TypeError:  # Raised when there is no <version> element.
        raise BadDataFile("The version number is missing from this file.")
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        book = None
    # Try to match on aliases, all of which must agree.
    books_matched = {}
    for scheme, value in aliases:
        for alias in Alias.objects.filter(scheme=scheme, value=value):
            if alias.book_id not in books_matched:
                books_matched[alias.book_id] = alias.book
            if len(books_matched) > 1:
                raise BadDataFile("The aliases in this file match more than one book.")
    # If a book was did not match by ID use the alias match if there was one, or create a new book.
    if book is None:
        if len(books_matched) == 1:
            book = books_matched.values()[0]
        else:
            book = Book.objects.create(pk=book_id)
    # Handle create/update of the book's edition.
    edition, created = Edition.objects.get_or_create(book_id=book.pk, version=edition_version)
    edition.title = book_element.findtext('title')
    edition.description = book_element.findtext('description')
    edition.save()
    # Handle create/update of the book's aliases.
    for scheme, value in aliases:
        book.aliases.get_or_create(scheme=scheme, value=value)
