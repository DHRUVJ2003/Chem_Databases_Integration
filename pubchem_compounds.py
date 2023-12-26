"""
/******************************************************************************
  This source file is part of the Avogadro project.

  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""
import argparse
import json
import sys
import requests
import pandas as pd
import pubchempy as pc
# Some globals:
debug = True

base_url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'
props=[
    'MolecularFormula', 'MolecularWeight', 'CanonicalSMILES', 'IsomericSMILES',
    'InChI', 'InChIKey', 'IUPACName', 'XLogP', 'ExactMass', 'MonoisotopicMass',
    'TPSA', 'Complexity', 'Charge', 'HBondDonorCount', 'HBondAcceptorCount',
    'RotatableBondCount', 'HeavyAtomCount', 'IsotopeAtomCount', 'AtomStereoCount',
    'DefinedAtomStereoCount', 'UndefinedAtomStereoCount', 'BondStereoCount',
    'DefinedBondStereoCount', 'UndefinedBondStereoCount', 'CovalentUnitCount',
    'Volume3D', 'XStericQuadrupole3D', 'YStericQuadrupole3D', 'ZStericQuadrupole3D',
    'FeatureCount3D', 'FeatureAcceptorCount3D', 'FeatureDonorCount3D',
    'FeatureAnionCount3D', 'FeatureCationCount3D', 'FeatureRingCount3D',
    'FeatureHydrophobeCount3D', 'ConformerModelRMSD3D', 'EffectiveRotorCount3D',
    'ConformerCount3D'
]

def check_url_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == requests.codes.ok
    except requests.ConnectionError:
        return False

# Example usage:

def getOptions():
    userOptions = {}
    userOptions['input_type'] = {}
    userOptions['input_type']['label'] = 'Choose Search Type'
    userOptions['input_type']['type'] = 'string'
    userOptions['input_type']['values'] =['SMILE','Compound Name']
    userOptions['input_type']['default'] = 'Compound Name'

    userOptions['search_compound'] = {}
    userOptions['search_compound']['label'] = 'Enter compound'
    userOptions['search_compound']['type'] = 'string'
    
    userOptions['Download'] = {}
    userOptions['Download']['label'] = 'Download SDF File(3D structure)'
    userOptions['Download']['type'] = 'boolean'
    userOptions['Download']['default'] = False
    return userOptions

def retrieve_compound(opts):
    input_type= opts['input_type']
    search_compound= opts['search_compound']
    download=bool(opts['Download'])

    if input_type=='Compound Name':
            properties = pc.get_properties(identifier=search_compound,namespace='name',properties=props)
            if properties==[]:
                return("The input record was not found")
            if download==True:
                pc.download('SDF', f'./{search_compound}.sdf', search_compound, namespace='name')
            preview=base_url+'/name/'+search_compound+'/PNG'
            if check_url_exists(preview):
                properties.append({'preview_link':preview})
            else:
                properties.append({'preview_link':"Image Not Found"})           
            return properties

    if input_type=='SMILE':
            properties = pc.get_properties(identifier=search_compound,namespace='smiles',properties=props)
            if properties==[]:
                return("The input record was not found")
            if download==True:
                pc.download('SDF', f'./{search_compound}.sdf', search_compound,namespace='smiles')
            preview=base_url+'/smiles/'+search_compound+'/PNG'
            if check_url_exists(preview):
                properties.append({'preview_link':preview})
            else:
                properties.append({'preview_link':"Image Not Found"})           
            return properties
    
            
def runCommand():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Prepare the result
    result = retrieve_compound(opts)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Search Compounds From PubChem')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-command', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Search Compounds From PubChem")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_command']:
        print(json.dumps(runCommand()))
