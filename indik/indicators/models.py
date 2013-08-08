from django.db import models

# Create your models here.

from mongoengine import *

#TODO: load from settings
connect('indik')


class FieldDescriptor(EmbeddedDocument):
    code = StringField(max_length=10, required=True)
    name = StringField(max_length=300, required=True)
    field_type = StringField(max_length=300, required=True)


class IndicatorDescriptor(Document):

    name = StringField(max_length=300, required=True)
    code = StringField(max_length=10, required=True, unique=True)
    fields = ListField(EmbeddedDocumentField(FieldDescriptor))
    value_field = StringField(max_length=200, required=True)


class IndicatorData(DynamicDocument):
    code = StringField(max_length=10, required=True)
    

class IndicatorClass(DynamicDocument):
    code = StringField(max_length=10, required=True)
    field_name = StringField(max_length=300, required=True)
    value = IntField()
    description = StringField(max_length=300)



def update_indicator(indicator_info, fields_descriptions, klasses_descriptions, data, update=False):

    code = indicator_info['code']

    try:
        ex_indicator_descriptor = IndicatorDescriptor.objects.get(code=code)
        ex_indicator_descriptor.delete()
    except:
        pass

    #ex_indicator_fields_descriptors = IndicatorDescriptor(code=code)
    try:
        ex_indicator_data = IndicatorData.objects(code=code)
        ex_indicator_data.delete()
    except Exception, e:
        print e
        pass
    try:
        ex_indicator_classes = IndicatorClass.objects(code=code)
        ex_indicator_classes.delete()
    except Exception, e:
        print e
        pass

    #ex_indicator_classes = IndicatorClasses.objects(code=code)

    
    fields_descriptors = []
    value_field = ""
    
    for desc in fields_descriptions:
        desc['code'] = code
        field_descriptor = FieldDescriptor(**desc)
        if desc['field_type'] == 'value':
            value_field = desc['name']
        fields_descriptors.append(field_descriptor)
    
    indicator_descriptor = IndicatorDescriptor(**indicator_info)
    indicator_descriptor.fields = fields_descriptors
    indicator_descriptor.value_field = value_field
    indicator_descriptor.save()

    klasses = {}
    for klass_description in klasses_descriptions:
        
        field_name = klass_description['field_name']
        klass_description['code'] = code
        klasses[field_name] = klasses.get(field_name, [])
        klasses[field_name].append(klass_description)
 
    for klass in klasses:
        items_list = klasses[klass]
        for it in items_list:
            kl = IndicatorClass(**it)
            kl.save()

    for d in data:
        d['code'] = code
        data_item = IndicatorData(**d)
        data_item.save()
    
    










