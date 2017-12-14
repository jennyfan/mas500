## Initialize
import mediacloud, json, datetime
from config import MY_API_KEY

mc = mediacloud.api.MediaCloud(MY_API_KEY)


## Research Question
## "Did US Mainstream Media sources talk about Trump or Clinton more in September 2016?"

## Trump
res = mc.sentenceCount('trump', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
print ("Trump: ", res['count']) # prints the number of sentences found


## Clinton
res = mc.sentenceCount('clinton', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
print ("Clinton: ", res['count']) # prints the number of sentences found 