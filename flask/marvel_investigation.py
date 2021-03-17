#!/usr/bin/env python
import os

import flask
import pymongo
import util.helper

# create a flask application
app = flask.Flask(__name__)

# create a mongodb client
client = pymongo.MongoClient("mongo:27017")

# define GET and POST methods for route / in flask app
@app.route('/', methods=['GET', 'POST'])
def marvel_investigation():

  try:

    # check if mongodb is up and running
    client.admin.command('ismaster')
    
    if flask.request.method == 'GET':
      
      # display welcome message, textbox and submit button 
      # in order to receive character name
      return util.helper.display_welcome()

    elif flask.request.method == 'POST':

      # get character name from input textbox in the form
      character_name = flask.request.form['text']

      # perform api call to receive required data
      character_data = util.helper.gather_data(character_name) 
      
      if character_data != None:

        # then post data to mongodb
        db = client.test_database
        db.marvel.insert_one(character_data)
        return f'{character_data.get("name")} data has been saved into the database successfully.<br><br>db collection name: {db.list_collection_names()}<br><br>number of documents in the collection: {db.marvel.count_documents({})}<br><br>document data: {db.marvel.find_one()}<br><br><a href="http://marvel.com">Data provided by Marvel. © 2021 MARVEL</a>'

      else:
        return 'Receiving data from Marvel has failed!'

    # this else statement is a placeholder for future development 
    # flask will allow only GET or POST as defined at the top
    else:
      return 'Unsupported Request type, please try GET or POST!'

  except Exception as e:
    return 'Server Error: ' + str(e) + '\n'

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 5000), debug=True)

