import os
import pickle as CP
import datetime
import json
import zlib

import dateutil.parser
import pymongo
import pysolr

from bson import json_util, ObjectId

from clean_html import remove_html_tags

def query_solr(query):
    SOLR_URL = "http://200.20.164.152:8983/solr"
    index_name = "mediacloud_articles"
    server = pysolr.Solr(os.path.join(SOLR_URL, index_name))
    results = server.search(query)
    hits = results.hits
    full_results = server.search(query, rows=hits)
    return full_results.docs

def filter_day(query_docs, day):
    valid_results = []
    for result in query_docs:
        if result.has_key('published'):
            data = dateutil.parser.parse(result['published'])
            if data > day:
                valid_results.append(result)
    return valid_results

def query_filter(query, day=dateutil.parser.parse('2013-12-01T00:00:00Z')):
    articles = query_solr(query)
    filter_articles = filter_day(articles, day)
    return filter_articles

def decompress_content(compressed_html):
    decompressed = zlib.decompress(compressed_html)
    orig_html = CP.loads(decompressed)
    return orig_html

def fetch_docs(ids, colname="articles"):
    client = pymongo.Connection("dirrj", 27017)
    db = client.MCDB
    coll = db[colname]
    cur = coll.find({"_id": {"$in": ids}},
                    {'_id': True, 'link_content': True, 'compressed': True,
                    'updated': True, 'published': True},
                    sort=[("_id", pymongo.DESCENDING)])
    return cur

if __name__ == '__main__':
    docs = query_filter('estupro')
    docs_ids = [ObjectId(d["_id"]) for d in docs]
    documents = fetch_docs(docs_ids)
    dic = []
    for document in documents:
        if document['compressed']:
            document_clean = decompress_content(document['link_content'])
        else:
            document_clean = document['link_content']
        try:
            text_document = remove_html_tags(document_clean)
        except:
            continue
	document['link_content'] = text_document
	dic.append(document)
        
    f = file('textos/artigo.txt', 'w')
    f.write(str(dic))
    f.close()

