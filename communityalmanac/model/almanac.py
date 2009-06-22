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

from __future__ import with_statement
from pylons import g
from pylons import session
from sqlalchemy import Table, Column, Integer, ForeignKey, Unicode, Numeric, Boolean, String, DateTime
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from sqlalchemy.schema import DDL
from sqlalchemy.orm import relation
from sqlalchemy.orm import exc
from sqlalchemy.orm import column_property
from sqlalchemy import and_

from uuid import uuid4

from meta import Base, storage_SRID
from sqlgeotypes import POINT
from shapely.geometry.point import Point
from shapely import wkb
from binascii import a2b_hex
import mimetypes
import PIL.Image
import pyproj
import meta
import os
import time
import uuid

# This is such a complicated trigger function, I was tempted to install
# PLPython to use python in the database.  Luckily, it's still pretty readable.
# You install this trigger on some table, and it updates another table's
# modified times. (e.g. A trigger on the pages table will update the almanacs
# table on INSERT, UPDATE, or DELETE.)  In addition, there's a special case to
# look for 'draft' pages and not cascade the modified time.
cascade_modify_time = """CREATE OR REPLACE FUNCTION cascade_modify_time_%(table)s() RETURNS trigger AS $cascade_modify_time_%(table)s$
  BEGIN
    IF '%(table)s' = 'almanacs' THEN
      IF TG_OP IN ('UPDATE', 'INSERT') THEN
        IF NOT NEW.published THEN
          -- We don't update the almanac when we modify draft pages.
          RETURN NULL;
        END IF;
      ELSE
        -- We're deleting a page, still need to perform the published check.
        IF NOT OLD.published THEN
          -- We don't update the almanac when we modify draft pages.
          RETURN NULL;
        END IF;
      END IF;
    END IF;
    IF TG_OP IN ('UPDATE', 'INSERT') THEN
      -- On delete, the foreign key can't have changed
      UPDATE %(table)s SET modified=CURRENT_TIMESTAMP WHERE id = NEW.%(foreign_key)s;
      IF TG_OP = 'UPDATE' THEN
        IF NEW.%(foreign_key)s != OLD.%(foreign_key)s THEN
          -- If we move an item from one entry to another, they have both been 'modified'
          UPDATE %(table)s SET modified=CURRENT_TIMESTAMP WHERE id = OLD.%(foreign_key)s;
        END IF;
      END IF;
    ELSE
      UPDATE %(table)s SET modified=CURRENT_TIMESTAMP WHERE id = OLD.%(foreign_key)s;
    END IF;
    RETURN NULL;
  END;
$cascade_modify_time_%(table)s$ LANGUAGE plpgsql;"""
cascade_modify_time_almanacs = DDL(cascade_modify_time,
                                  context=dict(table='almanacs', foreign_key='almanac_id'),
                                  on='postgres').execute_at('before-create', Base.metadata)
cascade_modify_time_pages = DDL(cascade_modify_time,
                                  context=dict(table='pages', foreign_key='page_id'),
                                  on='postgres').execute_at('before-create', Base.metadata)
cascade_modify_time_media = DDL(cascade_modify_time,
                                  context=dict(table='media', foreign_key='id'),
                                  on='postgres').execute_at('before-create', Base.metadata)

def normalize_url_slug(candidate):
    return candidate.replace(', ', '-').replace(' ', '').replace(',', '-')

class Almanac(Base):
    __tablename__ = 'almanacs'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    slug = Column(String, unique=True)
    location = Column(POINT(storage_SRID))
    creation = Column(DateTime, server_default=func.current_timestamp())
    # The auto-update field below doesn't do too much, because we almost always
    # update attached items, not the object itself.
    modified = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __init__(self, name=None, slug=None, location=None, id=None):
        self.name = name
        self.slug = slug
        if location:
            self.location = location
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<Almanac(id=%d, name=%s)>' % (self.id, self.name)

    @staticmethod
    def name_almanac(candidate):
        """name the almanac given the candidate name"""

        normalized = normalize_url_slug(candidate)
        try:
            Almanac.get_by_slug(normalized)
        except exc.NoResultFound:
            return normalized
        else:
            i = 1
            while True:
                name = u'%s-%s' % (normalized, i)
                try:
                    Almanac.get_by_slug(name)
                    i += 1
                except exc.NoResultFound:
                    return name

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
    def latest(limit=10, offset=0):
        return meta.Session.query(Almanac).join(Almanac.pages).order_by(Almanac.modified.desc()).distinct().limit(limit).offset(offset).all()

    @property
    def creation_date_string(self):
        """return the creation date formatted nicely as a string"""
        return self.creation.strftime('%B %d, %Y')

    @property
    def updated_date_string(self):
        """return the updated date formatted nicely as a string"""
        return self.modified.strftime('%B %d, %Y')

    @property
    def location_4326(self):
        if self._location_4326 is None:
            # God this is ugly Fix for bug #xxx in SQLAlchemy
            meta.Session.commit()
            if self._location_4326 is None:
                return None
        if ';' in self._location_4326:
            geom = wkb.loads(a2b_hex(self._location_4326.split(';')[-1]))
            geom.srid = 4326
            return geom
        else:
            geom = wkb.loads(a2b_hex(self._location_4326))
            geom.srid = 4326
            return geom
Almanac._location_4326 = column_property(func.st_transform(Almanac.location, 4326).label('_location_4326'))


class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    almanac_id = Column(Integer, ForeignKey('almanacs.id'))
    name = Column(Unicode)
    slug = Column(String)
    on_behalf_of = Column(Unicode)
    published = Column(Boolean, nullable=False)
    creation = Column(DateTime, server_default=func.current_timestamp())
    # The auto-update field below doesn't do too much, because we almost always
    # update attached items, not the object itself.
    modified = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __init__(self, name=None, slug=None, modified=None, created=None, almanac_id=None, user_id=None, id=None, published=False):
        self.name = name
        self.slug = slug
        self.published = published
        if modified:
            self.modified = modified
        if created:
            self.created = created
        if user_id is not None:
            self.user_id = user_id
        if almanac_id is not None:
            self.almanac_id = almanac_id
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<Page(id=%d, name=%s)>' % (self.id, self.name)

    @staticmethod
    def name_page(almanac, candidate):
        """name the page given the almanac and candidate name"""

        normalized = normalize_url_slug(candidate)
        try:
            Page.get_by_slug(almanac, normalized)
        except exc.NoResultFound:
            return normalized
        else:
            i = 1
            while True:
                name = u'%s-%s' % (normalized, i)
                try:
                    Page.get_by_slug(almanac, name)
                    i += 1
                except exc.NoResultFound:
                    return name

    @staticmethod
    def get_by_slug(almanac, slug):
        query = meta.Session.query(Page)
        query = query.filter(Page.almanac_id == almanac.id)
        query = query.filter(Page.slug == slug)
        return query.one()

    @staticmethod
    def latest(limit=10, offset=0):
        return meta.Session.query(Page).filter(Page.published==True).order_by(Page.modified.desc()).limit(limit).offset(offset).all()

    @property
    def creation_date_string(self):
        """return the creation date formatted nicely as a string"""
        return self.creation.strftime('%B %d, %Y')

    @property
    def first_story(self):
        """return the first story media item for the page, or a stub with empty text. This is useful to keep the templates simple."""
        for media in self.media:
            if isinstance(media, Story):
                return media
        return Story(text=u'')
    @property
    def first_image(self):
        """Return the first image media item for the page. Return None if the image doesn't exist"""
        for media in self.media:
            if isinstance(media, Image):
                return media

    def page_navigation(self):
        """return points to the prev and next pages, order by modification time

        will return a dictionary of 'prev' and 'next' keys"""

        def _find_navigation_for(q, ordering=asc):
            query = meta.Session.query(Page)
            query = query.filter(Page.almanac_id == self.almanac_id)
            query = query.filter(Page.published == True)
            query = query.filter(Page.id != self.id)
            query = query.filter(q)
            query = query.order_by(ordering(Page.modified))
            try:
                return query[:1][0]
            except (exc.NoResultFound, IndexError):
                return None
        return dict(next=_find_navigation_for(Page.modified >= self.modified),
                    prev=_find_navigation_for(Page.modified <= self.modified, desc),
                    )

    @property
    def map_media(self):
        """return a list of the map media associated with this page"""
        return [media for media in self.media if isinstance(media, Map)]

    @property
    def updated_date_string(self):
        """return the updated date formatted nicely as a string"""
        return self.modified.strftime('%B %d, %Y')

    @staticmethod
    def by_id(page_id):
        return meta.Session.query(Page).filter(Page.id == page_id).one()

Page.almanac = relation("Almanac", backref="pages", primaryjoin=and_(Page.almanac_id==Almanac.id, Page.published==True))
page_modify_trigger = DDL("""CREATE TRIGGER page_modify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON pages FOR EACH ROW
    EXECUTE PROCEDURE cascade_modify_time_almanacs();""", on='postgres').execute_at('after-create', Page.__table__)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey('pages.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    creation = Column(DateTime, server_default=func.current_timestamp())
    fullname = Column(Unicode)
    email = Column(Unicode)
    website = Column(Unicode)
    text = Column(Unicode)

    page = relation("Page", backref="comments")


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey('pages.id'), nullable=False)
    text = Column(Unicode)
    order = Column(Integer)
    discriminator = Column('type', String(50))
    modified = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    __mapper_args__ = dict(polymorphic_on=discriminator)

    page = relation("Page", backref="media")

    @staticmethod
    def by_id(media_id):
        return meta.Session.query(Media).filter(Media.id == media_id).one()
media_modify_trigger = DDL("""CREATE TRIGGER media_modify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON media FOR EACH ROW
    EXECUTE PROCEDURE cascade_modify_time_pages();""", on='postgres').execute_at('after-create', Media.__table__)


class PDF(Media):
    __tablename__ = 'pdfs'
    __mapper_args__ = dict(polymorphic_identity='pdf')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    path = Column(Unicode)
    filename = Column(Unicode)

    @property
    def url(self):
        import communityalmanac.lib.helpers as h
        return h.url_for('view_media_pdf', media=self)
pdf_modify_trigger = DDL("""CREATE TRIGGER pdf_modify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON pdfs FOR EACH ROW
    EXECUTE PROCEDURE cascade_modify_time_media();""", on='postgres').execute_at('after-create', PDF.__table__)


class Audio(Media):
    __tablename__ = 'audios'
    __mapper_args__ = dict(polymorphic_identity='audio')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    path = Column(Unicode)
    filename = Column(Unicode)

    @staticmethod
    def from_file(filename, fileobj=None, newpath=None, upload=None, page=None, **kwargs):

        if not newpath:
            newpath = g.audio_path

        mimetype, _ = mimetypes.guess_type(filename)

        if mimetype != 'audio/mpeg':
            raise ValueError(u'Invalid audio file')

        if upload:
            upload.make_file()
            fileobj = upload.file

        audio_data = fileobj.read()
        new_uuid = str(uuid.uuid4())
        path = os.path.join(newpath, new_uuid) + '.mp3'
        with open(path, 'w') as f:
            f.write(audio_data)

        audio = Audio(**kwargs)
        if page:
            page.media.append(audio)
            audio.order = len(page.media)
        else:
            audio.order = len(audio.page.media)
        audio.path = path
        audio.filename = filename
        return audio

    @property
    def url(self):
        import communityalmanac.lib.helpers as h
        return h.url_for('view_media_audio', media=self)
audio_modify_trigger = DDL("""CREATE TRIGGER audio_modify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON audios FOR EACH ROW
    EXECUTE PROCEDURE cascade_modify_time_media();""", on='postgres').execute_at('after-create', Audio.__table__)


class Video(Media):
    __tablename__ = 'videos'
    __mapper_args__ = dict(polymorphic_identity='video')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
video_modify_trigger = DDL("""CREATE TRIGGER video_modify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON videos FOR EACH ROW
    EXECUTE PROCEDURE cascade_modify_time_media();""", on='postgres').execute_at('after-create', Video.__table__)


class Image(Media):
    __tablename__ = 'images'
    __mapper_args__ = dict(polymorphic_identity='image')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    path = Column(Unicode)
    path_large = Column(Unicode)
    path_small = Column(Unicode)
    filename = Column(Unicode)

    @property
    def url(self):
        # we add a querystring to prevent the browser from caching
        qs = time.time()
        return '/media/view/image/%s/%s?%s' % (self.id, self.filename, qs)

    @property
    def large_url(self):
        # we add a querystring to prevent the browser from caching
        qs = time.time()
        return '/media/view/image/large/%s/%s?%s' % (self.id, self.filename, qs)

    @property
    def small_url(self):
        # we add a querystring to prevent the browser from caching
        qs = time.time()
        return '/media/view/image/small/%s/%s?%s' % (self.id, self.filename, qs)

    @staticmethod
    def from_file(filename, fileobj=None, newpath=None, upload=None, page=None, **kwargs):

        if not newpath:
            newpath = g.images_path

        _, ext = os.path.splitext(filename)
        mimetype, _ = mimetypes.guess_type(filename)

        if not mimetype.startswith('image/'):
            raise ValueError(u'Invalid image file %s' % filename)

        if upload:
            upload.make_file()
            fileobj = upload.file

        image_data = fileobj.read()
        new_uuid = str(uuid.uuid4())
        path = os.path.join(newpath, new_uuid) + ext
        with open(path, 'w') as f:
            f.write(image_data)

        image = Image(**kwargs)
        if page:
            page.media.append(image)
            image.order = len(page.media)
        else:
            image.order = len(image.page.media)
        image.path = path
        image.create_scales(newpath)
        image.filename = filename
        return image

    def create_scales(self, base_path):
        """create the necessary image scales from the saved path"""
        path = self.path
        assert path, "No image path set"

        _, ext = os.path.splitext(path)

        im = PIL.Image.open(self.path)

        new_uuid = str(uuid.uuid4())
        new_path = os.path.join(base_path, new_uuid) + ext
        self._create_scale(im, (520,1000), new_path)
        self.path_large = new_path

        new_uuid = str(uuid.uuid4())
        new_path = os.path.join(base_path, new_uuid) + ext
        self._create_scale(im, (75,75), new_path)
        self.path_small = new_path

    def _create_scale(self, im, size, new_path):
        scale = im.convert(dither=PIL.Image.NONE, palette=PIL.Image.ADAPTIVE)
        scale.thumbnail(size, PIL.Image.ANTIALIAS)
        scale.save(new_path)
        return scale

image_modify_trigger = DDL("""CREATE TRIGGER image_modify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON images FOR EACH ROW
    EXECUTE PROCEDURE cascade_modify_time_media();""", on='postgres').execute_at('after-create', Image.__table__)


class Story(Media):
    __tablename__ = 'stories'
    __mapper_args__ = dict(polymorphic_identity='story')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)

    def excerpt(self, n=140):
        """short version of the text, useful for displaying in lists"""
        text = self.text
        return text if len(text) < n else text[:n-4] + u' ...'
story_modify_trigger = DDL("""CREATE TRIGGER story_modify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON stories FOR EACH ROW
    EXECUTE PROCEDURE cascade_modify_time_media();""", on='postgres').execute_at('after-create', Story.__table__)

class Map(Media):
    __tablename__ = 'maps'
    __mapper_args__ = dict(polymorphic_identity='map')
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    location = Column(POINT(storage_SRID))

    @property
    def location_4326(self):
        if self._location_4326 is None:
            # God this is ugly Fix for bug #xxx in SQLAlchemy
            meta.Session.commit()
            if self._location_4326 is None:
                return None
        if ';' in self._location_4326:
            geom = wkb.loads(a2b_hex(self._location_4326.split(';')[-1]))
            geom.srid = 4326
            return geom
        else:
            geom = wkb.loads(a2b_hex(self._location_4326))
            geom.srid = 4326
            return geom
Map._location_4326 = column_property(func.st_transform(Map.location, 4326).label('_location_4326'))
map_modify_trigger = DDL("""CREATE TRIGGER map_modify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON maps FOR EACH ROW
    EXECUTE PROCEDURE cascade_modify_time_media();""", on='postgres').execute_at('after-create', Map.__table__)


# This is the association table for the many-to-many relationship between
# groups and permissions.
groups_permissions_table = Table('groups_permissions', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('permission_id', Integer, ForeignKey('permissions.id',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships.
users_groups_table = Table('users_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('group_id', Integer, ForeignKey('groups.id',
        onupdate="CASCADE", ondelete="CASCADE"))
)
class User(Base):

    #define name of table
    __tablename__ = "users"

    #its columns
    comment_fullname =   Column(Unicode(100))
    comment_website =    Column(Unicode(100))
    id =                 Column(Integer, primary_key=True)
    discriminator =      Column('type', String(50))
    creation =           Column(DateTime, server_default=func.current_timestamp())

    __mapper_args__ = dict(polymorphic_on=discriminator)

    pages = relation("Page", backref="user")

    def __init__(self, id=None):
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<User(id=%d, subtype=%s)>' % (self.id, self.discriminator)


class FullUser(User):
    __tablename__ = 'full_users'
    __mapper_args__ = dict(polymorphic_identity='full_user')

    id =                 Column(Integer, ForeignKey('users.id'), primary_key=True)
    username =           Column(Unicode(50), unique=True, nullable=False)
    email_address =      Column(Unicode(100), unique=True, nullable=True)
    reset_key =          Column(String(50), nullable=True)
    password =           Column(String(100), nullable=True)
    openid =             Column(String(200), nullable=True)

    def __init__(self, username=None, email_address=None, password=None, id=None):
        self.username = username
        self.email_address = email_address
        if password:
            self.set_password(password)
        self.reset_key = None
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

    def __repr__(self):
        return '<FullUser(id=%d, username=%s)>' % (self.id, self.username)

class AnonymousUser(User):
    __tablename__ = 'anonymous_users'
    __mapper_args__ = dict(polymorphic_identity='anonymous_user')
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    @property
    def username(self):
        return "Anonymous User"


class Group(Base):
    """An ultra-simple group definition."""
    __tablename__ = 'groups'

    id =   Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(16), unique=True)

    users = relation('User', secondary=users_groups_table, backref='groups')

class Permission(Base):
    """A relationship that determines what each Group can do"""
    __tablename__ = 'permissions'

    id =   Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(16), unique=True)

    groups = relation(Group, secondary=groups_permissions_table,
                      backref='permissions')

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
        return "{CRYPT}%s" % bcrypt.hashpw(cleartext_password, bcrypt.gensalt())

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

