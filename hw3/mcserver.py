import configparser, datetime, os, json, dateutil.parser

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

### load the settings file
config = configparser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

### set up logging
# logging.basicConfig(level=logging.DEBUG)
# logging.info("Starting the MediaCloud example Flask app!")


app = Flask(__name__)

## changing logging configuration
if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('errors.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('mediacloud app')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('mediacloud app')

### changing mediacloud settings.config api_key to heroku
heroku_api_key = os.environ.get('APIKEY')

### clean a mediacloud api client
mc = mediacloud.api.MediaCloud( heroku_api_key )
# mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

@app.route("/")
def home():
    return render_template("search-form.html")


@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']

    # now = datetime.datetime.now()
    startDate = request.form['startDate']
    endDate = request.form['endDate']

    ### get keywords from startDate and endDate, split by week
    results = mc.sentenceCount(keywords,
                               solr_filter=[mc.publish_date_query( datetime.datetime.strptime(startDate, "%Y-%m-%d"), datetime.datetime.strptime(endDate, "%Y-%m-%d") ), 'tags_id_media:9139487'],
                               split=True,
                               split_start_date=startDate,
                               split_end_date=endDate)

    ### results['count'] has # of entries
    ### results['split'] has entries split by day/week
    ### gap automatically calculated depending on scope of time between start and end date

    print(json.dumps(results['split'], indent=4, separators=(',', ': ')))
    
    ### clean data
    weekData = []

    ### push cleaned weeks to weekData
    for key in results['split']:
      ### filter out non-dates
      if len(key) > 5:

        weekDict= {}

        ### format date
        weekStr = key[:10]
        d = dateutil.parser.parse(weekStr)

        ### push cleaned data to weekData in format for d3plus
        weekDict["week"] = d.strftime('%Y-%m-%d')
        weekDict["value"] = results['split'][key]
        weekDict["name"] = keywords
        weekData.append(weekDict)

    # print(json.dumps(weekData))

    return render_template("search-results.html",
                           keywords=keywords,
                           sentenceCount=results['count'],
                           split_start_date=startDate,
                           split_end_date=endDate,
                           results=json.dumps(weekData))

if __name__ == "__main__":
    app.debug = True
    app.run()