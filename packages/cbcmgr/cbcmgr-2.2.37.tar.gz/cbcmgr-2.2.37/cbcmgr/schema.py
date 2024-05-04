##
##
from __future__ import annotations

import attr
import logging
import json
from attr.validators import instance_of as io
from .exceptions import SchemaFileError


@attr.s
class Inventory(object):
    inventory = attr.ib(validator=io(list))

    @classmethod
    def build(cls):
        return cls(
            []
        )

    def add_schema(self, schema: Schema):
        self.inventory.append(schema)
        return self

    def get(self, name: str):
        return next((s for s in self.inventory if s.name == name), None)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class Schema(object):
    name = attr.ib(validator=io(str))
    buckets = attr.ib(validator=io(list))
    rules = attr.ib(validator=io(list))

    @classmethod
    def build(cls, name: str):
        return cls(
            name,
            [],
            []
        )

    def add_bucket(self, bucket: Bucket):
        self.buckets.append(bucket)
        return self

    def add_rule(self, rule: Rule):
        self.rules.append(rule)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class BucketList(object):
    buckets = attr.ib(validator=io(list))

    @classmethod
    def build(cls):
        return cls(
            []
        )

    def add(self, resource: Bucket):
        self.buckets.append(resource)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class RuleList(object):
    rules = attr.ib(validator=io(list))

    @classmethod
    def build(cls):
        return cls(
            []
        )

    def add(self, resource: Rule):
        self.rules.append(resource)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class Bucket(object):
    name = attr.ib(validator=io(str))
    scopes = attr.ib(validator=io(list))

    @classmethod
    def build(cls, name: str):
        return cls(
            name,
            []
        )

    def add_scope(self, scope: Scope):
        self.scopes.append(scope)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class Scope(object):
    name = attr.ib(validator=io(str))
    collections = attr.ib(validator=io(list))

    @classmethod
    def build(cls, name: str):
        return cls(
            name,
            []
        )

    def add_collection(self, collection: Collection):
        self.collections.append(collection)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class Collection(object):
    name = attr.ib(validator=io(str))
    schema = attr.ib(validator=attr.validators.instance_of((list, dict, str)))
    idkey = attr.ib(validator=io(str))
    primary_index = attr.ib(validator=io(bool))
    override_count = attr.ib(validator=io(bool))
    index_names = attr.ib(validator=io(list))
    record_count = attr.ib(validator=attr.validators.optional(io(int)), default=None)
    key_format = attr.ib(validator=attr.validators.optional(io(str)), default=None)
    indexes = attr.ib(validator=attr.validators.optional(io(list)), default=None)

    @classmethod
    def from_config(cls, json_data: dict):
        id_key = json_data.get("idkey")
        schema_data = json_data.get("schema")
        if type(schema_data) == list:
            schema_list = [CollectionDoc.from_config(s) for s in schema_data]
        else:
            schema_list = [
                CollectionDoc.from_config(
                    {
                        "id_key": id_key,
                        "override_count": json_data.get("override_count"),
                        "record_count": json_data.get("record_count"),
                        "doc": schema_data
                    }
                )
            ]
        return cls(
            json_data.get("name"),
            schema_list,
            id_key,
            json_data.get("primary_index"),
            json_data.get("override_count"),
            [],
            json_data.get("record_count"),
            json_data.get("key_format"),
            [i for i in json_data.get("indexes")]
            )

    def add_index_name(self, name: str):
        self.index_names.append(name)

    def remove_index_name(self, name: str):
        self.index_names.remove(name)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class CollectionDoc(object):
    doc = attr.ib(validator=io(dict))
    override_count = attr.ib(validator=attr.validators.optional(io(bool)), default=None)
    id_key = attr.ib(validator=attr.validators.optional(io(str)), default=None)
    record_count = attr.ib(validator=attr.validators.optional(io(int)), default=None)

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(

            json_data.get("doc"),
            json_data.get("override_count"),
            json_data.get("id_key"),
            json_data.get("record_count")
            )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class Rule(object):
    name = attr.ib(validator=io(str))
    type = attr.ib(validator=io(str))
    id_field = attr.ib(validator=io(str))
    foreign_key = attr.ib(validator=io(str))
    primary_key = attr.ib(validator=io(str))
    sql = attr.ib(validator=io(str))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("name"),
            json_data.get("type"),
            json_data.get("id_field"),
            json_data.get("foreign_key"),
            json_data.get("primary_key"),
            json_data.get("sql")
            )

    @property
    def as_dict(self):
        return self.__dict__


class ProcessSchema(object):

    def __init__(self, filename: str = None, json_data: dict = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.filename = filename
        self.inventory_data = json_data
        self._inventory = Inventory.build()

        if filename:
            try:
                with open(self.filename, 'r') as schema_file:
                    self.inventory_data = json.load(schema_file)
                    schema_file.close()
            except KeyError:
                raise SchemaFileError(f"schema file {self.filename}: syntax error")
            except Exception as err:
                raise SchemaFileError(f"can not open schema file {self.filename}: {err}")

        if not self.inventory_data:
            raise SchemaFileError(f"no schema data")

    def inventory(self):
        inventory_builder = Inventory.build()
        for entry in self.inventory_data.get("inventory"):
            for schema in entry:
                schema_builder = Schema.build(schema)
                for bucket in entry[schema].get("buckets", []):
                    bucket_name = bucket.get("name")
                    bucket_scopes = bucket.get("scopes")
                    bucket_builder = Bucket.build(bucket_name)
                    for scope in bucket_scopes:
                        scope_name = scope.get("name")
                        scope_collections = scope.get("collections")
                        scope_builder = Scope.build(scope_name)
                        for collection in scope_collections:
                            collection_builder = Collection.from_config(collection)
                            scope_builder.add_collection(collection_builder)
                        bucket_builder.add_scope(scope_builder)
                    schema_builder.add_bucket(bucket_builder)
                for rule in entry[schema].get("rules", []):
                    rule_builder = Rule.from_config(rule)
                    schema_builder.add_rule(rule_builder)
                inventory_builder.add_schema(schema_builder)
        return inventory_builder
