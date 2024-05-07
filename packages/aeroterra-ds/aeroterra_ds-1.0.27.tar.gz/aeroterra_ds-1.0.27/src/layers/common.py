def ordinal(n: int):
    """
    Returns the string representing the ordinal of the number n. 
    
    Parameters:
        - n: int wanting to cast to ordinal
    """
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


def get_item(gis, item_id):
    """
    Find Item from its id
    
    Parameters:
        - gis: GIS object logged in where to search from
        - item_id: ID of the asked item
    
    Returns the item object inside the service
    """
    gis_item = gis.content.get(item_id)
    if gis_item is None:
        raise Exception(f"Layer (Id: {item_id}) Can't Be Found")
    
    return gis_item

def get_layer(gis, layer_id, number=None):
    """
    Find Layer from its id
    
    Parameters:
        - gis: GIS object logged in where to search from
        - layer_id: ID of the asked layer
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    
    Returns the layer object inside the service
    """
    layer_item = get_item(gis, layer_id)
    
    layers = layer_item.layers
    if len(layers) > 1 and number is None:
        raise Exception(f"Layer (Id: {layer_id}) Has Too Many Layers ({layers})")
    elif len(layers) == 0:
        raise Exception(f"Layer (Id: {layer_id}) Has NO Layers")
    
    if number is None:
        return layers[0]
    
    if len(layers) < number:
        ord_num = ordinal(number)
        raise Exception(f"Layer (Id: {layer_id}) Has Not Enough Layers To Get the {ord_num} One [{len(layers)} < {number}]")
        