# encoding: utf-8

import datetime
from sqlalchemy import Column, Table, ForeignKey, orm
from sqlalchemy import types as _types
from sqlalchemy.sql.expression import false
from ckan.model import meta, Package, domain_object


__all__ = [u"PackageReferenceLink", u"package_reference_link_table"]

package_reference_link_table = Table(
    u"package_reference_link",
    meta.metadata,
    Column(u"id", _types.Integer, primary_key=True, nullable=False),
    Column(u"package_name", _types.UnicodeText, ForeignKey(u"package.name"), nullable=False),
    Column(u"doi", _types.UnicodeText, nullable=False),    
    Column(u"create_at", _types.DateTime, default=datetime.datetime.utcnow, nullable=False),
    Column(u"citation", _types.UnicodeText),
    Column(u"authors", _types.UnicodeText),
    Column(u"title", _types.UnicodeText),
    Column(u"year", _types.UnicodeText),
    Column(u"url", _types.UnicodeText),
    Column(u"ref_type", _types.UnicodeText),
    Column(u"publisher", _types.UnicodeText),
    Column(u"place", _types.UnicodeText),
    Column(u"journal", _types.UnicodeText),
    Column(u"volume", _types.UnicodeText),
    Column(u"issue", _types.UnicodeText),
    Column(u"page", _types.UnicodeText),
    Column(u"proceeding", _types.UnicodeText),
    Column(u"access_date", _types.UnicodeText),
    Column(u"organization", _types.UnicodeText),
    Column(u"thesis_type", _types.UnicodeText),
    Column(u"conference_date", _types.UnicodeText),
    
)


class PackageReferenceLink(domain_object.DomainObject):
    def __init__(self, reference_object):
        self.package_name = reference_object.get('package_name')
        self.doi = reference_object.get('doi')        
        self.create_at = reference_object.get('create_at')
        self.citation = reference_object.get('citation')
        self.authors = reference_object.get('authors')
        self.title = reference_object.get('title')
        self.year = reference_object.get('year')
        self.url = reference_object.get('url')
        self.ref_type = reference_object.get('ref_type')
        self.publisher = reference_object.get('publisher')
        self.place = reference_object.get('place')
        self.journal = reference_object.get('journal')
        self.volume = reference_object.get('volume')
        self.issue = reference_object.get('issue')
        self.page = reference_object.get('page')
        self.proceeding = reference_object.get('proceeding')
        self.access_date = reference_object.get('access_date')
        self.organization = reference_object.get('organization')
        self.thesis_type = reference_object.get('thesis_type')
        self.conference_date = reference_object.get('conference_date')

    
    @classmethod
    def get_by_package(cls, name, autoflush=True):
        if not name:
            return None

        exists = meta.Session.query(cls).filter(cls.package_name==name).first() is not None
        if not exists:
            return false
        query = meta.Session.query(cls).filter(cls.package_name==name)
        query = query.autoflush(autoflush)
        record = query.all()
        return record
    

    @classmethod
    def get_by_id(cls, id, autoflush=True):
        if not id:
            return None

        exists = meta.Session.query(cls).filter(cls.id==id).first() is not None
        if not exists:
            return false
        query = meta.Session.query(cls).filter(cls.id==id)
        query = query.autoflush(autoflush)
        record = query.first()
        return record

    
    def get_package(self):
        return self.package



meta.mapper(
    PackageReferenceLink,
    package_reference_link_table,
    properties={
        u"package": orm.relation(
            Package, backref=orm.backref(u"package_reference_link", cascade=u"all, delete, delete-orphan")
        )
    },
)







