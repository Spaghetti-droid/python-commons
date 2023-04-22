def addToDicList(dic:dict, key:any, value:any):
    """Adds the position of the operation given by index to a list in dic

    Args:
        dic (dict): dictionary to update
        key (any): key for the list to append to
        value (any): value to append
    """
    listForKey = dic.get(key)
    if not listForKey:
        listForKey = []
        dic[key] = listForKey
    listForKey.append(value) 