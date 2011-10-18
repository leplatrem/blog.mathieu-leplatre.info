Une démo squelettique de python Flask CouchDB 
#############################################

:date: 2011-10-11 11:30
:tags: python, couchdb, flask
:lang: fr

Avec ``Flask`` et ``Couchdb`` (e.g. `Flask-CouchDB <http://packages.python.org/Flask-CouchDB/>`_),
on peut faire rapidement des trucs amusants, voire très utiles !

Voici un **squelette** d'application, fonctionnel, qui stocke et récupère des objets crées à partir de posts HTTP.

.. code-block :: python

    import simplejson
    from flask import Flask, g, request
    from couchdb.design import ViewDefinition
    import flaskext.couchdb


    app = Flask(__name__)

    """
    CouchDB permanent view
    """
    docs_by_author = ViewDefinition('docs', 'byauthor', 
                                    'function(doc) { emit(doc.author, doc); }')

    """
    Retrieve docs
    """
    @app.route("/<author_id>/docs")
    def docs(author_id):
        docs = []
        for row in docs_by_author(g.couch)[author_id]:
            docs.append(row.value)
        return simplejson.dumps(docs)

    """
    Add doc
    """
    @app.route("/<author_id>/add", methods=['POST'])
    def add_doc(author_id):
        try:
            # Build doc with posted values
            doc = { 'author': author_id }
            doc.update(request.form)
            # Insert into database
            g.couch.save(doc)
            state = True
        except Exception, e:
            state = False
        return simplejson.dumps({'ok': state})

    """
    Flask main
    """
    if __name__ == "__main__":
        app.config.update(
            DEBUG = True,
            COUCHDB_SERVER = 'http://localhost:5984/',
            COUCHDB_DATABASE = 'docsdemo'
        )
        manager = flaskext.couchdb.CouchDBManager()
        manager.setup(app)
        manager.add_viewdef(docs_by_author)  # Install the view
        manager.sync(app)
        app.run(host='0.0.0.0', port=5000)

J'ai déposé ce snippet sur `Gist <https://gist.github.com/1277655>`_ si besoin.

On peut attaquer l'application avec ``curl`` :

.. code-block :: bash

    $ curl -d "title=Globalia&year=2004" http://0.0.0.0:5000/jc.rufin/add
    {"ok": true}
    $ curl -d "title=Red%20Brazil&contest=goncourt" http://0.0.0.0:5000/jc.rufin/add
    {"ok": true}
    
    $ curl http://0.0.0.0:5000/jc.rufin/docs
    [{"title": ["Globalia"], "year": ["2004"], "author": "jc.rufin", "_rev": "1-3195...fbc8", "_id": "dec81d...1733c"},
    {"title": ["Red Brazil"], "contest": ["goncourt"], "author": "jc.rufin", "_rev": "1-7b15...a9a2", "_id": "dec81dc...17c0c"}]

N'oubliez pas de colorier les cases à votre guise, sinon ce squelette ne sert à rien, le JSON étant déjà la langue maternelle de CouchDB.



