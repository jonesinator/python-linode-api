import linode.objects
from linode import util


def get_mapping(id):
    id_map = { 
        'lnde': linode.objects.Linode,
        'disk': linode.objects.Disk,
        'dist': linode.objects.Distribution,
        'serv': linode.objects.Service,
        'dctr': linode.objects.Datacenter,
        'stck': linode.objects.StackScript,
        'conf': linode.objects.Config,
        'krnl': linode.objects.Kernel,
        'ljob': linode.objects.Job,
        'imag': linode.objects.Image,
    }

    parts = id.split('_')

    if not len(parts) == 2:
        return False

    if parts[0] in id_map:
        return id_map[parts[0]]
    return None

def make(id, parent_id=None):
    """
    Makes an api object based on an id.  The type depends on the mapping.
    """
    c = get_mapping(id)

    if c:
        if issubclass(c, linode.objects.DerivedBase):
            return c(id, parent_id)
        else:
            return c(id)
    return None

def make_list(json_arr, parent_id=None):
    result = []

    for obj in json_arr:
        if not 'id' in obj:
            continue
        o = make(obj['id'], parent_id=parent_id)
        o._populate(obj)
        result.append(o)

    return result

def make_paginated_list(json, key, parent_id=None):
    l = make_list(json[key], parent_id=parent_id)
    p = util.PaginatedList(key, page=l, max_pages=json['total_pages'], \
         total_items=json['total_results'], parent_id=parent_id)
    return p
