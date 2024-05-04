from typing import Union, Callable, Iterable, Literal


# TODO: tests
def drop_duplicates(iterable, method:Literal['set', 'sorted set', 'generator', 'manual', 'other']='sorted set'):
    method = method.lower()
    if method == 'set':
        return type(iterable)(set(iterable))
    elif method == 'sorted set':
        return list(sorted(set(iterable), key=lambda x: iterable.index(x)))
    elif method == 'generator':
        seen = set()
        for item in seq:
            if item not in seen:
                seen.add(item)
                yield item
    elif method == 'manual':
        dups = {}
        newlist = []
        for x in biglist:
            if x['link'] not in dups:
                newlist.append(x)
                dups[x['link']] = None
    elif method == 'other':
        seen_links = set()
        for index in len(biglist):
            link = biglist[index]['link']
            if link in seen_links:
                del(biglist[index])
            seen_links.add(link)
    else:
        raise ValueError(f'Unknown method {method}. Options are: (set, sorted set, generator, manual, other)')

# TODO: I guess this is useful? Figure out how the dict + operator works first
def addDicts(*dicts):
    """ Basically the same thing as Dict.update(), except returns a copy
        (and can take multiple parameters)
    """
    rtn = {}
    for d in dicts:
        rtn.update(d)
    return rtn

# TODO: make this actually work
class MultiAccessDict(dict):
    """ Exactly the same thing as a regular dict, except you can get and set multiple items
        at once, and it returns a list of the asked for items, or sets all of the items to
        the specified value
    """
    def __getitem__(self, *keys):
        if len(keys) == 0:
            raise KeyError("No input parameters given")
        return [super().__getitem__(key) for key in keys]

    def __setitem__(self, *keys, value):
        pass
        # todo('figure out how the setitem parameters work')
        # return [super().__setitem__(key) for key in keys]
