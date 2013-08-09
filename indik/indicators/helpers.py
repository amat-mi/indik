import json




MONGO_GROUP_AGGREGATIONS = ['addToSet', 'first', 'last', 'max', 'min', 'avg', 'sum', 'push']


def serialize_mongo_object(o):
    
    if hasattr(o, "to_json"):
        o = dict(json.loads(o.to_json()))
    
    if '_id' in o:
        if isinstance(o['_id'], dict):
            for key in o['_id']:
                o[key] = o['_id'][key]
        del o['_id']
    
    return o


def iterator_serializer(iterable, properties_callbacks={}):
    for x in iterable:
        out = serialize_mongo_object(x)
        for k in properties_callbacks:
            out[k] = properties_callbacks[k](out, k)
        yield out
        


def get_lookup_query(filters):
    
    out  = {}
    for fi in filters:
        #
        pieces = fi.split("__")
        p = len(pieces)
        if p == 1:
            out[fi] = filters[fi]
        elif p == 2:
            inner_dict = { "$%s"%pieces[1] : filters[fi] }
            out[pieces[0]] = out.get(pieces[0], {})
            out[pieces[0]].update(inner_dict)

    return out


def group_by_query(collection, operator, target_field, group_fields=[], filter={}, sort_like_groups=True):
    
    if operator not in MONGO_GROUP_AGGREGATIONS:
        raise ValueError("aggregation operator must be one of: " + ", ".join(MONGO_GROUP_AGGREGATIONS))
    
    if group_fields:
        id_dict = {}
        for field in group_fields:
            id_dict[field] = '$%s' % field

    else:
        id_dict = None
    

    operator_dict = { '$%s' % operator : '$%s' % target_field }
    
    group_dict = {'$group' : {'_id' : id_dict, target_field : operator_dict} }

    pipeline = []
    if filter:
        match_dict = {'$match' : filter }
        pipeline.append(match_dict)    

    if sort_like_groups and group_fields:
        sort_fields = dict()
        for g in group_fields:
            sort_fields[g] = -1
        sort_dict = {'$sort' : sort_fields}
        pipeline.append(sort_dict)


    pipeline.append(group_dict)

    q =  collection.aggregate(pipeline)
    return q['result']





