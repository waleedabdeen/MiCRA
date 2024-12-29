from . import treeify
import pandas as pd
import re

def aggregate_bottom_up(root_node):    
    children_nodes = cs_tree.children(root_node.identifier)

    if children_nodes != None and len(children_nodes) > 0:
        for child in children_nodes:
            child_description = aggregate_bottom_up(child)
            root_node.tag = root_node.tag + ", " + child_description            

        return root_node.tag

    else:
        return root_node.tag

def aggregate_top_down(root_node):    
    children_nodes = cs_tree.children(root_node.identifier)

    if children_nodes != None and len(children_nodes) > 0:
        for i, child in enumerate(children_nodes):
            # do not aggregate the root discription
            if root_node.tag not in ['Tillgångssystem', 'Konstruktiva system', 'Grundfunktioner och Komponenter']:
                children_nodes[i].tag = children_nodes[i].tag + ", " + root_node.tag

            aggregate_top_down(child)


def aggregate_nodes(df_taxonomy: object, cs: str, table: str, how: str, content_index: int):
    global cs_tree
    if cs == 'CoClass':
        cs_tree = treeify.coclass_from_df(df_taxonomy,'coclass', content_index)
    elif cs == 'SB11':
        cs_tree = treeify.sb11_from_df(df_taxonomy,'sb11', content_index)
    elif cs == 'Tele': 
        cs_tree = treeify.coclass_from_df(df_taxonomy,'tele', content_index)
    else:
        raise Exception("invalid cs")
    
    if how == 'bottomup':
        aggregate_bottom_up(cs_tree.get_node(table))
    elif how == 'topdown':
        aggregate_top_down(cs_tree.get_node(table))
    else:
        raise Exception("invalid input (how)")
    
    return cs_tree


def remove_dummy_nodes(taxonomy: pd.DataFrame, desc_key: str):
    taxonomy = taxonomy.drop(taxonomy.loc[taxonomy['name_eng'].str.startswith('Dummy')].index, axis=0)
    taxonomy[desc_key] = taxonomy[desc_key].apply(lambda desc: re.sub(r'\b[d,D]ummy([a-z-\,,A-Z\,]+)?', r'', desc))
    taxonomy[desc_key] = taxonomy[desc_key].apply(lambda desc: re.sub(r"\s+", " ", desc))                                                                                               
    return taxonomy