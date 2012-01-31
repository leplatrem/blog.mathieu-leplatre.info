Access a JSON webservice with Qt C++
####################################

:date: 2011-12-16 17:00
:tags: c++, qt, json
:lang: en

*Original post at* `Makina Corpus <http://makina-corpus.org>`_

Webservices are everywhere ! There are relevant in many situations, and
accessing them from your Qt C++ application is not an heresy. 

I will present here a very simple way to retrieve a JSON from a GET request. 


=============
HTTP Requests
=============


Using `QNetworkAccessManager <http://developer.qt.nokia.com/doc/qt-4.7/qnetworkaccessmanager.html>`_ is
a piece of cake :

.. code-block :: c++

    QNetworkAccessManager networkManager;
     
    QUrl url("http://gdata.youtube.com/feeds/api/standardfeeds/most_popular?v=2&alt=json");
    QNetworkRequest request;
    request.setUrl(url);
    
    QNetworkReply* currentReply = networkManager.get(request);  // GET



But, note that a slightly more generic approach would be to build the ``QUrl`` from a parameters list :


.. code-block :: c++

    QUrl url("http://gdata.youtube.com/feeds/api/standardfeeds/");
    QString method = "most_popular";
    url.setPath(QString("%1%2").arg(url.path()).arg(method));
    
    QMap<QString, QVariant> params;
    params["alt"] = "json";
    params["v"] = "2";
    
    foreach(QString param, params.keys()) {
        url.addQueryItem(param, params[param].toString());
    }


============
Parsing JSON
============

Get yourself a *slot* to parse the ``QNetworkReply`` : 

.. code-block :: c++

    connect(&networkManager, SIGNAL(finished(QNetworkReply*)), this, SLOT(onResult(QNetworkReply*)));


.. code-block :: c++

    void YourClass::onResult(QNetworkReply* reply)
    {
        if (m_currentReply->error() != QNetworkReply::NoError)
            return;  // ...only in a blog post

        QString data = (QString) reply->readAll();

        QScriptEngine engine;
        QScriptValue result = engine.evaluate(data);
        
        /* 
          Google YouTube JSON looks like this : 
          
          {
            "version": "1.0",
            "encoding": "UTF-8",
            "feed": {
              ..
              ..
              "entry": [{
                "title": {
                    "$t": "Nickelback- When We Stand Together"
                },
                "content": {
                    "type": "application/x-shockwave-flash",
                    "src": "http://www.youtube.com/v/76vdvdll0Y?version=3&f=standard&app=youtube_gdata"
                },
                "yt$statistics": {
                    "favoriteCount": "29182",
                    "viewCount": "41513706"
                },
                ...
                ...
              },
              ...
              ...
              ]
            }
          }
        */

        // Now parse this JSON according to your needs !
        QScriptValue entries = result.property("feed").property("entry");
        QScriptValueIterator it(entries);
        while (it.hasNext()) {
            it.next();
            QScriptValue entry = it.value();
            
            QString link = entry.property("content").property("src").toString();
            int viewCount = entry.property("yt$statistics").property("viewCount").toInteger();
            
            // Do something with those...
        }
    }


That's it :)

If you want more complexity, and don't mind adding extra-dependencies, check out Tomasz Siekierda's `QtWebService <http://gitorious.org/qwebservice>`_ ! 
