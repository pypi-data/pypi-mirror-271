import json, yaml, os
from classes.DB import db
from classes.Segment import Segment
import pandas as pd
import numpy as np

def parse_json(config_file: str, verbose: bool = False):
    """Parse JSON file."""
    
    # sanity check
    assert os.path.isfile(config_file), f"Config file not found: {config_file}"

    # read json file
    with open(config_file, 'r') as f:
        meta = json.load(f)
    

    #
    segmentations = []
    categories = {}
    category_occurences = {}
    types = {}
    type_ocurences = {}
    modifiers = {}
    modifier_occurences = {}


    # ietrate segments
    for segments in meta['segmentAttributes']:
        for segment in segments:

            # desc
            desc = segment['SegmentDescription']
            
            #
            category = segment['SegmentedPropertyCategoryCodeSequence']
            category_code = category['CodeValue']
                
            if not category_code in categories:
                categories[category_code] = category
                category_occurences[category_code] = 1
            else:
                assert categories[category_code] == category
                category_occurences[category_code] += 1
            
            #
            typ = segment['SegmentedPropertyTypeCodeSequence']
            typ_code = typ['CodeValue']
            
            if not typ_code in types:
                types[typ_code] = typ
                type_ocurences[typ_code] = 1
            else:
                assert types[typ_code] == typ
                type_ocurences[typ_code] += 1
                
            #
            if 'SegmentedPropertyTypeModifierCodeSequence' in segment:
                mod = segment['SegmentedPropertyTypeModifierCodeSequence']
                mod_code = mod['CodeValue']
                
                if not mod_code in modifiers:
                    modifiers[mod_code] = mod
                    modifier_occurences[mod_code] = 1
                else:
                    if modifiers[mod_code] != mod:
                        print(modifiers[mod_code])
                        print(mod)
                        
                        print("-----")
                    
                    assert modifiers[mod_code] == mod
                    modifier_occurences[mod_code] += 1
            else:
                if verbose:
                    print('--> segment without mod', desc)
                mod_code = None

            # id,name,category,type,modifyer,color

            segmentations.append({
                'id': '?',
                'name': desc,
                'category': category_code,
                'type': typ_code,
                'modifier': mod_code,
                'color': segment['recommendedDisplayRGBValue'],
                'desc': desc   
            })
            
        if verbose:
            print(desc)

    if verbose:
        print('---')
        print('segmentations')
        print(segmentations)
        print('---')
        print('categories')
        print(categories)
        print(category_occurences)
        print('---')
        print('types')
        print(types)
        print(type_ocurences)
        print('---')
        print('modifiers')
        print(modifiers)
        print(modifier_occurences)

    return {
        'segments': segmentations,
        'categories': categories,
        'category_occurences': category_occurences,
        'types': types,
        'type_ocurences': type_ocurences,
        'modifiers': modifiers,
        'modifier_occurences': modifier_occurences
    }

        
def identify_new_and_updated_segments(d):
   
    # convert detected dictionaries into pandas data frame
    detected_categories = pd.DataFrame(list(d['categories'].values())).astype({'CodeValue': int}).set_index('CodeValue')
    detected_types = pd.DataFrame(list(d['types'].values())).astype({'CodeValue': int}).set_index('CodeValue')
    detected_modifiers = pd.DataFrame(list(d['modifiers'].values())).astype({'CodeValue': int}).set_index('CodeValue') if len(d['modifiers'].values()) > 0 else pd.DataFrame([])

    # check for new categories
    new_categories = detected_categories[~detected_categories.index.isin(db.categories.index)]
    new_types = detected_types[~detected_types.index.isin(db.types.index)]
    new_modifiers = detected_modifiers[~detected_modifiers.index.isin(db.modifiers.index)] if detected_modifiers is not None else None

    # check for new segments based on category, type and modifier
    new_segmentations = []
    for segB in d['segments']:
        found_duplicate = False
        for _, segA in db.segmentations.iterrows():
            segA = dict(segA.replace(np.nan, None))

            if int(segA['category']) == int(segB['category']) and int(segA['type']) == int(segB['type']) and int(segA['modifier'] or 0) == int(segB['modifier'] or 0):
                found_duplicate = True
                break
            
        if not found_duplicate:
            new_segmentations.append(segB)

    # return
    return {
        'new_categories': new_categories,
        'new_types': new_types,
        'new_modifiers': new_modifiers,
        'new_segmentations': new_segmentations
    }




if __name__ == "__main__":
    print(os.getcwd())
    
    #
    print(db.categories)

    # parse json config
    parsed = parse_json('example_data/dicomseg_metadata.json')

    # search for new data
    found = identify_new_and_updated_segments(parsed)

    # present new data and ask user for confirmation
    print("findings:")
    print("new categories:", len(found['new_categories'].index))
    print("new types:", len(found['new_types'].index))
    print("new modifiers:", len(found['new_modifiers'].index))
    print("new segmentations:", len(found['new_segmentations']))
    print()

    print("new categories:")
    print(found['new_categories'])
    print()

    print("new types:")
    print(found['new_types'])
    print()

    print("new modifiers:")
    print(found['new_modifiers'])
    print()
    
    print("new segmentations:")
    print(found['new_segmentations'])
