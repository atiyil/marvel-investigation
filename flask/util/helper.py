#!/usr/bin/env python
import requests
import json
import hashlib
import time
import bz2

def display_welcome():
  ''' This function provides the welcome message at start '''

  return '''
  Welcome to the investigation of Marvel characters!<br><br>
  Please provide a name to get a character's id, description and picture<br>
  along with all characters in the same comics with the character:<br>
  <form method="POST">
    <input name="text">
    <input type="submit">
  </form>

  <a href="http://marvel.com">Data provided by Marvel. © 2021 MARVEL</a>
  '''

def compute_hash(PUBLIC_KEY):
  ''' This function computes the hash required by restful GET requests '''

  # TODO: provide private key in a secure way: 
  # already encrypted by an env variable?
  # use a vault?
  # use keyring?
  PRIVATE_KEY = b'BZh91AY&SY\x10cM\x16\x00\x00(\xc9\x00\xc0\x00\x7f\xc0?\x00\x00\x01\xa0\x00TSL\x8cLLA\xa4\xd3\x081\x05\xd1\xa4\xc3\x8dRf\x8e\x06V\xf5\x13V\xe2#\xc1\x9e\x15\x95\xd9\xf4\xbc E\xdb\x02\x16\x1f\x17rE8P\x90\x10cM\x16'
  ts = str(int(time.time()))

  hash_string = ts + bz2.decompress(PRIVATE_KEY).decode('UTF-16') + PUBLIC_KEY

  # prepare the hash value for GET request 
  # by encoding epoch TimeStamp (ts) along with Public & Private keys
  # and then converting the result hash to a hexadecimal string
  result = hashlib.md5(hash_string.encode()).hexdigest()
  return result, ts

def gather_data(character_name):
  ''' This function gathers character data by performing restful GET requests '''
  PUBLIC_KEY = 'aa2c172156bfb936dff98d84bb76d84b'

  thehash, ts = compute_hash(PUBLIC_KEY)
  request_url = f'https://gateway.marvel.com:443/v1/public/characters?limit=100&nameStartsWith={character_name}&ts={ts}&apikey={PUBLIC_KEY}&hash={thehash}'
  main_character_response = requests.get(request_url)

  # TODO: handle other status codes
  if main_character_response.status_code == 200:

    character_data = {}

    # if there are multiple results, use the first one
    main_character = json.loads(main_character_response.content.decode('UTF-8')).get('data').get('results')[0]
    
    character_data.update({'id':main_character.get('id')})
    character_data.update({'name':main_character.get('name')})
    character_data.update({'description':main_character.get('description')})
    character_data.update({'thumbnail':main_character.get('thumbnail')})
    character_data.update({'characters':{}})

    # perform GET request to receive all comics that main character appears
    # notice that previous GET call provides at most 20 comics, not all
    thehash, ts = compute_hash(PUBLIC_KEY)
    request_url = f'https://gateway.marvel.com:443/v1/public/characters/{character_data.get("id")}/comics?limit=100&ts={ts}&apikey={PUBLIC_KEY}&hash={thehash}'
    all_comics_response = requests.get(request_url)

    # TODO: handle other status codes
    if all_comics_response.status_code == 200:
      all_comics = json.loads(all_comics_response.content.decode('UTF-8')).get('data').get('results')
      
      # find all comics for the main character and populate the dictionary character_data
      for comic in all_comics:
        comic_characters = comic.get('characters').get('items')

        # for each character in the comic, check if this is the main character
        # or already an existing one in the dictionary character_data
        for character in comic_characters:
          if character_data.get('name') != character.get('name') \
          and character_data.get('characters').get(character.get('name')) == None:

            # if this is a new character, pull the data by a GET request
            # and add it to the dictionary character_data
            thehash, ts = compute_hash(PUBLIC_KEY)
            request_url = f'https://gateway.marvel.com:443/v1/public/characters?limit=100&name={character.get("name")}&ts={ts}&apikey={PUBLIC_KEY}&hash={thehash}'
            character_response = requests.get(request_url)

            # TODO: handle other status codes
            if character_response.status_code == 200:

              # update the dictionary by new character
              the_character = json.loads(character_response.content.decode('UTF-8')).get('data').get('results')[0]
              character_data.get('characters').update({str(the_character.get('id')):{\
                'name':the_character.get('name'),\
                'description': the_character.get('description'),\
                'thumbnail': the_character.get('thumbnail')}})

            else:
              return None

    else:
      return None

    return character_data

  else:
    return None
