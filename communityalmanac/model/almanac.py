# Community Almanac - A place for your stories.
# Copyright (C) 2009  Douglas Mayle, Robert Marianski,
# Andy Cochran, Chris Patterson

# This file is part of Community Almanac.

# Community Almanac is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Community Almanac is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Community Almanac.  If not, see <http://www.gnu.org/licenses/>.

from pylons import session
from sqlalchemy import Column, Integer, ForeignKey, Unicode, Numeric, Boolean, String, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relation
from sqlalchemy.orm import exc
from sqlalchemy import and_

from uuid import uuid4

from meta import Base, storage_SRID
from sqlgeotypes import POINT
import meta

class Almanac(Base):
    __tablename__ = 'almanacs'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    slug = Column(String, unique=True)
    location = Column(POINT(storage_SRID))
    creation = Column(DateTime, server_default=text('current_timestamp'))

    def __init__(self, name=None, slug=None, id=None):
        self.name = name
        self.slug = slug
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<Almanac(id=%d, name=%s)>' % (self.id, self.name)

    def new_page(self, user, **fields):
        assert('almanac_id' not in fields)
        assert('user_id' not in fields)
        userid = session.setdefault('userid', None)
        if isinstance(user, FullUser) and userid:
            # Check to see if there is an Anonymous user and suck that page
            # in...
            anon_user = meta.Session.query(AnonymousUser).get(userid)
            if anon_user:
                user.pages += anon_user.pages
                meta.Session.delete(anon_user)
                meta.Session.commit()
            # Don't forget to clean up the session
            session['userid'] = None
            session.save()
        try:
            page = meta.Session.query(Page).filter(and_(Page.published == False, Page.almanac_id == self.id, Page.user_id == user.id)).one()
            modified = False
            for field, value in fields.iteritems():
                if hasattr(page, field) and getattr(page, field) != value:
                    setattr(page, field, value)
                    modified = True
            if modified:
                meta.Session.commit()
            return page
        except exc.MultipleResultsFound:
            # It's time to combine these pages and chew bubblegum... and I'm
            # all out of gum...
            pages = meta.Session.query(Page).filter(and_(Page.published == False, Page.almanac_id == self.id, Page.user_id == user.id))
            winner = pages[0]
            name = winner.name
            for loser in pages[1:]:
                if loser.name != name:
                    winner.name += ', %s' % loser.name
                winner.media += loser.media
                meta.Session.commit()
                meta.Session.delete(loser)
            else:
                meta.Session.commit()
            return winner
        except exc.NoResultFound:
            pass
        page = Page(published=False, almanac_id=self.id, user_id=user.id, **fields)
        meta.Session.add(page)
        meta.Session.commit()
        return page

    @classmethod
    def get_by_slug(cls, slug):
        return meta.Session.query(Almanac).filter(Almanac.slug == slug).one()

    @staticmethod
    def latest():
        #FIXME we'll need to store created/modified times
        return meta.Session.query(Almanac).all()

    @property
    def creation_date_string(self):
        """return the creation date formatted nicely as a string"""
        return self.creation.strftime('%B %d, %Y')

    @property
    def updated_date_string(self):
        """return the updated date formatted nicely as a string"""
        #XXX this is stubbed out to be the creation date for now
        #XXX change this to the updated time when we store that
        return self.creation_date_string

class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    almanac_id = Column(Integer, ForeignKey('almanacs.id'))
    name = Column(Unicode)
    slug = Column(String)
    description = Column(Unicode)
    published = Column(Boolean, nullable=False)
    creation =  Column(DateTime, server_default=text('current_timestamp'))


    def __init__(self, name=None, slug=None, description=None, almanac_id=None, user_id=None, id=None, published=False):
        self.name = name
        self.slug = slug
        self.published = False
        if user_id is not None:
            self.user_id = user_id
        if almanac_id is not None:
            self.almanac_id = almanac_id
        if description is not None:
            self.description = description
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<Page(id=%d, name=%s)>' % (self.id, self.name)

    @classmethod
    def get_by_slug(cls, almanac, slug):
        query = meta.Session.query(Page)
        query = query.filter(Page.almanac_id == almanac.id)
        query = query.filter(Page.slug == slug)
        return query.one()
Page.pages = relation("Almanac", backref="pages", primaryjoin=and_(Page.almanac_id==Almanac.id, Page.published==True))


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey('pages.id'))
    creation = Column(DateTime, server_default=text('current_timestamp'))
    fullname = Column(Unicode)
    email = Column(Unicode)
    website = Column(Unicode)
    text = Column(Unicode)

    comments = relation("Page", backref="comments")


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey('pages.id'), nullable=False)
    text = Column(Unicode)
    order = Column(Integer)
    discriminator = Column('type', String(50))

    __mapper_args__ = dict(polymorphic_on=discriminator)

    media = relation("Page", backref="media")

    @staticmethod
    def by_id(media_id):
        return meta.Session.query(Media).filter(Media.id == media_id).one()


class PDF(Media):
    __tablename__ = 'pdfs'
    __mapper_args__ = dict(polymorphic_identity='pdf')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    path = Column(Unicode)

class Sound(Media):
    __tablename__ = 'sounds'
    __mapper_args__ = dict(polymorphic_identity='sound')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    path = Column(Unicode)

class Image(Media):
    __tablename__ = 'images'
    __mapper_args__ = dict(polymorphic_identity='image')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    flickr_id = Column(String)

class Story(Media):
    __tablename__ = 'stories'
    __mapper_args__ = dict(polymorphic_identity='story')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)

class Map(Media):
    __tablename__ = 'maps'
    __mapper_args__ = dict(polymorphic_identity='map')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    location = Column(POINT(storage_SRID))

    maps = relation("Page", backref="maps")

class User(Base):

    #define name of table
    __tablename__ = "users"

    #its columns
    comment_fullname =   Column(Unicode(100))
    comment_website =    Column(Unicode(100))
    id =                 Column(Integer, primary_key=True)
    discriminator =      Column('type', String(50))

    __mapper_args__ = dict(polymorphic_on=discriminator)

    pages = relation("Page", backref="user")

    def __init__(self, id=None):
        if id is not None:
            self.id = id


class FullUser(User):
    __tablename__ = 'full_users'
    __mapper_args__ = dict(polymorphic_identity='full_user')

    id =                 Column(Integer, ForeignKey('users.id'), primary_key=True)
    username =           Column(Unicode(50), nullable=False)
    email_address =      Column(Unicode(100), nullable=True)
    reset_key =          Column(String(50), nullable=True)
    password =           Column(String(100), nullable=True)
    openid =             Column(String(200), nullable=True)
    super_user =         Column(Boolean, nullable=False, default=False)

    def __init__(self, username=None, email_address=None, password=None, id=None):
        self.username = username
        self.email_address = email_address
        if password:
            self.set_password(password)
        self.reset_key = None
        self.super_user = False
        if id is not None:
            self.id = id

    def authenticate(self, password):
        if False:
            # Appropriate test for old style passwords that authenticates
            self.password = default_password_hash(password)
            meta.Session.commit()
        return default_password_compare(password, self.password)

    def generate_key(self):
        if not self.reset_key:
            self.reset_key = str(uuid4())

    def set_password(self, password):
        self.password = default_password_hash(password)


class AnonymousUser(User):
    __tablename__ = 'anonymous_users'
    __mapper_args__ = dict(polymorphic_identity='anonymous_user')
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)


def default_password_compare(cleartext_password, stored_password_hash):
    # Hashing functions work on bytes, not strings, so while unicode passwords
    # with only ascii characters work, it could blow up.  We'll catch that in
    # all cases.
    assert isinstance(cleartext_password, str)
    assert isinstance(stored_password_hash, str)

    # This functin assumes that stored hashes starting with {scheme} are hashed
    # passwords, and all other passwords are cleartext.  Because of this
    # assumption, cleartext passwords that begin with {scheme} will generate
    # errors for users.  In this case, it is recommended to migrate the
    # cleartext passwords to bcrypt.
    scheme = None
    if stored_password_hash.startswith('{'):
        # Look for the password scheme.
        try:
            endtoken = stored_password_hash.index('}')
            scheme = stored_password_hash[1:endtoken].upper()
            stored_password_hash = stored_password_hash[endtoken+1:]
        except ValueError:
            scheme = 'CLEAR'
    else:
        scheme = 'CLEAR'

    from base64 import urlsafe_b64encode, urlsafe_b64decode

    # The support is getting better and better.  We now support five schemes
    # for hashing, Salted Blowfish Crypt (bcrypt), Salted SHA256, Salted SHA-1,
    # standard SHA-1, and cleartext passwords.  The general encoding scheme
    # follows RFC 2307 standard for storage of encrypted passwords.  The
    # standard format looks like this: {scheme}encryptedpassword where the
    # encrypted password is base64 encoded in a url safe way.  In the case of
    # bcrypt, encrypted password is slightly different, as it is of the form:
    # {CRYPT}$2a$<2 digit complexity>$<22 bytes salt><31 bytes hash>  The salt
    # and hash are base64 encoded as in other schemes.
    # Caveats: SHA256 hashing requires Python 2.5 or pycrypto
    #          bcrypt hashing requires bcrypt module.

    if scheme == 'CRYPT':
        try:
            from bcrypt import bcrypt
        except ImportError:
            # We blow up so that Sysadmins can detect the error quicker and get
            # the problem fixed.
            raise NotImplementedError("Unable to load bcrypt module for Blowfish hashes")
        return stored_password_hash == bcrypt.hashpw(cleartext_password, stored_password_hash)

    # The salted SHA hashes work the same.  The only difference is how to find
    # the suitable hash module.
    if scheme == 'SSHA256':
        try:
            from hashlib import sha256
        except ImportError:
            try:
                from Crypto.Hash.SHA256 import new as sha256
            except ImportError:
            # We blow up so that Sysadmins can detect the error quicker and get
            # the problem fixed.
                raise NotImplementedError("Unable to load suitable module for SHA256 hashes")
        try:
            hash_bytes = urlsafe_b64decode(stored_password_hash)
        except TypeError:
            # This will happen if database is using unschemed cleartext
            # passwords, and the cleartext password is a bad encoding of a
            # schemed hash
            raise ValueError("Invalid password hash.")
        # SHA 256 is 256-bits of output (32 bytes)
        salt = hash_bytes[32:]
        hasher = sha256(cleartext_password)
        hasher.update(salt)
        return stored_password_hash == urlsafe_b64encode(hasher.digest() + salt)

    if scheme == 'SSHA':
        try:
            from hashlib import sha1
        except ImportError:
            try:
                from sha import new as sha1
            except ImportError:
                return False
        try:
            hash_bytes = urlsafe_b64decode(stored_password_hash)
        except TypeError:
            # This will happen if database is using unschemed cleartext
            # passwords, and the cleartext password is a bad encoding of a
            # schemed hash
            raise ValueError("Invalid password hash.")
        # SHA-1 is 160-bits of output (20 bytes)
        salt = hash_bytes[20:]
        hasher = sha1(cleartext_password)
        hasher.update(salt)
        return stored_password_hash == urlsafe_b64encode(hasher.digest() + salt)

    if scheme == 'SHA':
        try:
            from hashlib import sha1
        except ImportError:
            try:
                from sha import new as sha1
            except ImportError:
                # We blow up so that Sysadmins can detect the error quicker and
                # get the problem fixed.
                raise NotImplementedError("Unable to find hashing algorithm SHA-1 or stronger.")

        hasher = sha1(cleartext_password)
        # We need to support the legacy, hex format for existing hashes.
        # Luckily, we can unambiguously tell the difference, as SHA-1 hashes
        # always end with '=' (an invalid hex character) when base64 encoded.
        if stored_password_hash.endswith('='):
            computed_hash = urlsafe_b64encode(hasher.digest())
        else:
            computed_hash = hasher.hexdigest()
        return stored_password_hash == computed_hash

    if scheme == 'CLEAR':
        return stored_password_hash == cleartext_password
    # While we support reading of unsalted SHA-1 and cleartext passwords for
    # legacy databases support, we won't generate these unsecure formats.

    # Oops, unsupported scheme...
    # We blow up so that Sysadmins can detect the error quicker and get the
    # problem fixed.
    raise NotImplementedError("Unrecognized Hash Scheme: %s" % scheme)

def default_password_hash(cleartext_password, scheme='BESTAVAILABLE'):
    # Hashing functions work on bytes, not strings, so while unicode passwords
    # with only ascii characters work, it could blow up.  We'll catch that in
    # all cases.
    assert isinstance(cleartext_password, str)

    try:
        scheme = scheme.upper()
    except AttributeError:
        pass
    from base64 import urlsafe_b64encode
    from os import urandom

    # The support is getting better and better.  We now support three salted
    # schemes for hashing, Salted Blowfish Crypt (bcrypt), Salted SHA256,
    # and Salted SHA-1. While the compare function can ready unsalted SHA-1 and
    # cleartext passwords, we don't support generating them.  The general
    # encoding scheme follows RFC 2307 standard for storage of encrypted
    # passwords.  The standard format looks like this:
    # {scheme}encryptedpassword where the encrypted password is base64 encoded
    # in a url safe way.  In the case of bcrypt, encrypted password is slightly
    # different, as it is of the form:
    # {CRYPT}$2a$<2 digit complexity>$<22 bytes salt><31 bytes hash>  The salt
    # and hash are base64 encoded as in other schemes.
    # Caveats: SHA256 hashing requires Python 2.5 or pycrypto
    #          bcrypt hashing requires bcrypt module.

    if scheme == 'BESTAVAILABLE':
        # Since bcrypt is the strongest cryptographically, we'll default to it
        # if available.
        try:
            from bcrypt import bcrypt
        except ImportError:
            bcrypt = None
        if bcrypt:
            return "{CRYPT}%s" % bcrypt.hashpw(cleartext_password, bcrypt.gensalt())

        # Next up is the SHA family, we'll try SHA256 which is available in
        # Python >= 2.5 or with the pycrypto module.  Without that, we'll fall
        # back to SHA-1.
        try:
            from hashlib import sha256 as hashalgorithm
            scheme = 'SSHA256'
        except ImportError: # Python < 2.5 #pragma NO COVERAGE
            try:
                # On Python < 2.5, we pull sha256 from pycrypto if it's installed.
                from Crypto.Hash.SHA256 import new as hashalgorithm
                scheme = 'SSHA256'
            except ImportError:
                # If we couldn't import sha256 above, we know we can't pull
                # sha1 from the same module, so we'll try to pull from the
                # older sha module.
                try:
                    from sha import new as hashalgorithm
                    scheme = 'SSHA'
                except ImportError:
                    raise NotImplementedError("Unable to find hashing algorithm SHA-1 or stronger.")

        # The algorithm is the same for the entire SHA family, pretty easy.
        salt = urandom(4)
        hasher = hashalgorithm(cleartext_password)
        hasher.update(salt)
        return "{%s}%s" % (scheme, urlsafe_b64encode(hasher.digest() + salt))

    # Now that the ugly default case is out of the way, we handle the explicit
    # cases.
    if scheme == 'CRYPT':
        try:
            from bcrypt import bcrypt
        except ImportError:
            raise NotImplementedError("Unable to load bcrypt module for Blowfish hashes")
        return "{CRYPT}%s" % bcrypt.hashpw(password, bcrypt.gensalt())

    # The salted SHA hashes work the same.  The only difference is how to find
    # the suitable hash module.
    if scheme == 'SSHA256':
        try:
            from hashlib import sha256
        except ImportError:
            try:
                from Crypto.Hash.SHA256 import new as sha256
            except ImportError:
                raise NotImplementedError("Unable to load suitable module for SHA256 hashes")
        salt = urandom(4)
        hasher = sha256(cleartext_password)
        hasher.update(salt)
        return "{SSHA256}%s" % urlsafe_b64encode(hasher.digest() + salt)

    if scheme == 'SSHA':
        try:
            from hashlib import sha1
        except ImportError:
            try:
                from sha import new as sha1
            except ImportError:
                raise NotImplementedError("Unable to load suitable module for SHA-1 hashes")
        salt = urandom(4)
        hasher = sha1(cleartext_password)
        hasher.update(salt)
        return "{SSHA}%s" % urlsafe_b64encode(hasher.digest() + salt)

    # While we support reading of unsalted SHA-1 and cleartext passwords for
    # legacy databases support, we won't generate these unsecure formats.

    # Oops, unsupported scheme...
    raise NotImplementedError("Unrecognized Hash Scheme: %s" % scheme)

