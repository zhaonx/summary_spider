import pymongo

asia_uri = 'mongodb://asia.mongo.pub.spider:nVPVEfWNsekzD7XOKnAPq3hlDty2sRkt@pub.mongo.asia.nb.com:27017/?replicaSet=pub&readPreference=secondaryPreferred&authSource=admin'
db = pymongo.MongoClient(asia_uri)['spider_i18n']
col_dic = {'60second': db['60second_summary'],
           'bshort': db['bshortnews_summary'],
           'npr': db['npr_summary']}

latest_60second = db['60second_summary'].find().sort("pubilish_time", -1)[0].get('origin_url')
latest_bshort = db['bshortnews_summary'].find().sort("pubilish_time", -1)[0].get('origin_url')
latest_npr = db['npr_summary'].find().sort("pubilish_time", -1)[0].get('origin_url')
