import os

API_KEY_PUBLIC = '4686d80fe1c32de602b1128803798b21'
API_KEY_PRIVATE = 'dfbcca1008a39fff581b73e69ac9344e46ef8328'
HASH_MD5 = '3bf6f147cc8248b8d6ccf073e23b1455'
TS = '1'

URL = f'http://gateway.marvel.com/v1/public/characters?ts={TS}&apikey={API_KEY_PUBLIC}&hash={HASH_MD5}'

AWS = {
    'USR_AWS':'arielmfeldman_coderhouse',
    'USR_PASS':'D40Svx2I4h',
    'DATABASE':'data-engineer-database',
    'HOST':'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
    'PORT':5439,
    'SCHEMA':'arielmfeldman_coderhouse',
}

os.environ['API_KEY_PUBLIC']= API_KEY_PUBLIC
os.environ['API_KEY_PRIVATE']= API_KEY_PRIVATE
os.environ['HASH_MD5']= HASH_MD5
os.environ['TS']= TS
os.environ['URL']= URL
os.environ['AWS_USR']=AWS['USR_AWS']
os.environ['AWS_HOST']=AWS['HOST']
os.environ['AWS_PORT']=AWS['PORT']
os.environ['AWS_SCHEMA']=AWS['SCHEMA']
os.environ['AWS_DATABASE']=AWS['DATABASE']
 