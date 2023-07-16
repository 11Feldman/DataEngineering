API_KEY_PUBLIC = '4686d80fe1c32de602b1128803798b21'
API_KEY_PRIVATE = 'dfbcca1008a39fff581b73e69ac9344e46ef8328'
HASH_MD5 = '3bf6f147cc8248b8d6ccf073e23b1455'
TS = '1'

URL = {
    'characters':f'http://gateway.marvel.com/v1/public/characters?ts={TS}&apikey={API_KEY_PUBLIC}&hash={HASH_MD5}',
    'comics_1':f'http://gateway.marvel.com/v1/public/comics?',
    'comics_2':f'&ts={TS}&apikey={API_KEY_PUBLIC}&hash={HASH_MD5}',
    'creators':f'http://gateway.marvel.com/v1/public/creators?ts={TS}&apikey={API_KEY_PUBLIC}&hash={HASH_MD5}',
    'events':f'http://gateway.marvel.com/v1/public/events?ts={TS}&apikey={API_KEY_PUBLIC}&hash={HASH_MD5}',
    'series':f'http://gateway.marvel.com/v1/public/series?ts={TS}&apikey={API_KEY_PUBLIC}&hash={HASH_MD5}',
    'stories':f'http://gateway.marvel.com/v1/public/stories?ts={TS}&apikey={API_KEY_PUBLIC}&hash={HASH_MD5}',

}

AWS = {
    'USR_AWS':'arielmfeldman_coderhouse',
    'USR_PASS':'D40Svx2I4h',
    'DATABASE':'data-engineer-database',
    'HOST':'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
    'PORT':5439,
    'SCHEMA':'arielmfeldman_coderhouse',
}
