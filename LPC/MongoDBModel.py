from mongoengine import Document, DateTimeField, DictField, StringField, ListField, FloatField, ReferenceField, IntField

__author__ = 'teddy'
'''
{
  "_id" : "e790a256-d686-4bb0-9d4e-7b27de8a211b",
  "first_sample_timestamp" : ISODate("2015-12-01T13:12:18.953Z"),
  "last_sample_timestamp" : ISODate("2016-01-18T16:33:23.649Z"),
  "metadata" : {
    "description" : "default"
  },
  "meter" : [{
      "counter_name" : "poll.firewall",
      "counter_unit" : "firewall",
      "counter_type" : "gauge"
    }],
  "project_id" : "bd78fccc0a1b48a8bf09797a9c5031a9",
  "resource_name" : null,
  "source" : "openstack",
  "user_id" : null
}

'''
class Resource(Document):
    first_sample_timestamp=DateTimeField()
    last_sample_timestamp=DateTimeField()
    metadata=DictField()
    meter=ListField()
    project_id=StringField()
    resource_name=StringField()
    source=StringField()
    user_id=StringField()

"""
"_id" : ObjectId("569b7fc3fe9b1e4ca8667f71"),
  "counter_name" : "poll.volume",
  "resource_id" : "aa109798-ba88-4e8f-87bf-29b2b228ea29",
  "timestamp" : ISODate("2016-01-17T11:48:38.45Z"),
  "T" : 300,
  "period_start" : ISODate("2016-01-17T11:43:38.45Z"),
  "avg" : 1.0,
  "unit" : "volume",
  "count" : 5,
  "max" : 1.0,
  "user_id" : null,
  "val" : 1.0,
  "min" : 1.0,
  "sum" : 5.0,
  "period_end" : ISODate("2016-01-17T11:48:38.45Z"),
  "project_id" : "0a7ed23e9eca4be0ae497ff0bd98a76a",
  "message_id" : "59dbe026-bd10-11e5-aa46-6e064a600541"
"""
class Statistics300(Document):
    counter_name=StringField()
    resource_id=StringField()
    timestamp=DateTimeField()
    T=StringField()
    period_start=DateTimeField()
    avg=FloatField()
    unit=StringField()
    count=IntField()
    max=FloatField()
    user_id=StringField()
    val=FloatField()
    min=FloatField()
    sum=FloatField()
    period_end=DateTimeField()
    project_id=StringField()
    message_id=StringField()

class Statistics86400(Document):
    counter_name=StringField()
    resource_id=StringField()
    timestamp=DateTimeField()
    T=StringField()
    period_start=DateTimeField()
    avg=FloatField()
    unit=StringField()
    count=IntField()
    max=FloatField()
    user_id=StringField()
    val=FloatField()
    min=FloatField()
    sum=FloatField()
    period_end=DateTimeField()
    project_id=StringField()
    message_id=StringField()