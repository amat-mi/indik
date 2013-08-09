from django.db import models

# Create your models here.

from mongoengine import *

#TODO: load from settings
connect('indik')


class FieldDescriptor(EmbeddedDocument):

    name = StringField(max_length=300, required=True)
    field_type = StringField(max_length=300, required=True)


class IndicatorDescriptor(Document):

    name = StringField(max_length=300, required=True)
    code = StringField(max_length=10, required=True, unique=True)
    fields = ListField(EmbeddedDocumentField(FieldDescriptor))
    value_field = StringField(max_length=200, required=True)

    def get_klasses(self):
        return [x.name for x in self.fields if x.field_type=='class']

    def get_klasses_dict(self):
        out  = {}
        klasses = self.get_klasses()
        for k in klasses:
            klass_dict = {}
            items = IndicatorClass.objects(field_name=k)
            
            for item in items:
                #print item
                klass_dict[getattr(item, 'value')] = item.description
            out[k] = klass_dict
        return out


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

    
    fields_descriptors = []
    value_field = ""
    
    for desc in fields_descriptions:
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
    
    










