from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response, jsonify
import os
import cPickle as CP
import datetime
import json
import zlib
import re

import dateutil.parser
import pymongo
import pysolr

from bson import json_util, ObjectId

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

@app.route("/")
def root():
    return render_template('index.html')

@app.route('/similarity/data.json')
def json_similarity():
    data = ''
    with open(os.path.join(APP_STATIC, 'data.json')) as f:
        data = data + f.read()
    articles = json.loads(data)

    for art in articles:
        art['summary'] = art['summary'][:250]
        art['summary'] = art['summary'].replace('style', 'data')

    return json.dumps(articles), 200

@app.route('/timeline/')
def timeline():
    return render_template('pages/indextimeline.html')

@app.route('/timeline/data.jsonp')
def json_timeline():
    data = ''
    with open(os.path.join(APP_STATIC, 'data.json')) as f:
        data = data + f.read()
    articles = json.loads(data)
    for art in articles:
        art['published'] = datetime.date.fromtimestamp(art['published']['$date']/1000.).strftime("%Y,%m,%d")
    
    # Caso tenha parent na query string, filtraremos a lista de artigos
    parent = request.args.get('parent', '')
    if parent:
        # Guardamos o id do parent
        selectedArticles = [parent]
        
        # Pegamos o objeto do parent na lista de artigos para termos acesso aos ids dos filhos
        parentObj = filter(lambda a: a['_id']['$oid'] == parent , articles)
        
        # Pegamos todos os ids dos filhos do parent
        for child in parentObj[0]['childrenId']:
            selectedArticles.append(child['$oid'])

        # Agora selecionamos os ids relevantes da lista de artigos (parent + filhos)
        hasChildren = len(parentObj[0]['childrenId']) > 0
        if hasChildren:
            articles = filter(lambda a: a['_id']['$oid'] in selectedArticles , articles)
        else:
            articles = parentObj
    dados = render_template('pages/timeline.json', busca='Estupro', articles=articles)
    return Response(dados, mimetype='application/json')

@app.errorhandler(500)
def page_not_found(e):
    return e, 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)