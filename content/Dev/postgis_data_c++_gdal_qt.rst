PostGIS data in C++ using GDAL and Qt
#####################################

:date: 2011-08-23 10:25
:tags: c++, qt, postgis, gdal
:lang: en

*Original post at* `Makina Corpus <http://makina-corpus.org>`_

I did not find any ready-to-use snippets on the Web on this matter, so if
you are lucky enough, you'll find this one.

The objective is to read GIS geometries from a PostGIS database and manipulate
them in C++. I use Qt here, but it is not really a prerequisite, it just
helps a lot. Well, actually, it saves lives.


===================
Database Connection
===================

.. code-block :: c++

    m_db = QSqlDatabase::addDatabase("QPSQL");
    m_db.setHostName("host");
    m_db.setDatabaseName("dbname");
    m_db.setUserName("user");
    m_db.setPassword("pass");

Do not close the database at the end of each query. 

.. code-block :: c++

    m_db.close();
    m_db = QSqlDatabase();  // reinitialize for real


Shut it down like this in your class' destructor or you may have errors like 
*QSqlDatabasePrivate::removeDatabase: connection 'qt_sql_default_connection' is still in use, all queries will cease to work* 



===============
Records Reading
===============

.. code-block :: c++
   
    QSqlQueryModel* model = new QSqlQueryModel();

    model->setQuery("SELECT id, ST_AsBinary(the_geom) AS the_geom "
                    "FROM table");

    int numRows = model->rowCount();
    
    for (int i=0; i<numRows; ++i) {
        // Read fields
        qlonglong id = record(i).value("id").toLongLong();
        QByteArray wkb = record(i).value("the_geom").toByteArray();
    
        // Process !
        processRecord(id, wkb);
    }

QByteArray uses `implicit sharing <http://doc.qt.nokia.com/latest/implicit-sharing.html>`_
and can be passed as argument without being copied. 
    

==================
Geometries Parsing
==================

In this part, we rely on `GDAL (Geospatial Data Abstraction Library) <http://www.gdal.org>`_ 
`OGRSpatialReference <http://www.gdal.org/ogr/osr_tutorial.html>`_.

It provides an API to access geometries coordinates etc.


.. code-block :: c++

    #include "ogrsf_frmts.h" // GDAL
    ...
    ...
    
    void Class::processRecord(qlonglong id, QByteArray wkb)
    {
        OGRSpatialReference osr;
        OGRGeometry *geom = NULL;
        
        // Parse WKB
        OGRErr err = OGRGeometryFactory::createFromWkb((unsigned char*)wkb.constData(), &osr, &geom);
        if (err != OGRERR_NONE){
            // process error, like emit signal
        }
        
        // Analyse geometry by type and process them as you wish
        OGRwkbGeometryType type = wkbFlatten(geom->getGeometryType());
        switch(type) {
            case wkbLineString: {
                OGRLineString *poRing = (OGRLineString*)geom;
                
                // Access line string nodes for example :
                int numNode = poRing->getNumPoints();
                OGRPoint p;
                for(int i = 0;  i < numNode;  i++) {
                    poRing->getPoint(i, &p);
                    qDebug() << p.getX() << p.getY();
                }
                break;
            }
            case wkbMultiLineString:
            {
                OGRGeometryCollection  *poCol = (OGRGeometryCollection*) geom;
                int numCol = poCol->getNumGeometries();
                for(int i=0; i<numCol; i++) {
                    // Access line length for example : 
                    qDebug() << poCol->getGeometryRef(i)->get_Length();
                }
                break;
            }
            default:
                // process error, like emit signal
        }
        
        // Clean-up
        OGRGeometryFactory::destroyGeometry(geom);
    }

In this snippet, I only process linestrings, but all `geometry types are available <http://www.gdal.org/ogr/ogr__core_8h.html#800236a0d460ef66e687b7b65610f12a>`_.
Consider writing a recursive function for geometry collections and so forth...

Hope this helped !

