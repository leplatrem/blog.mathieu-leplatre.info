Automatic blog publishing using Python and XML-RPC
##################################################

:date: 2008-12-01 13:37
:tags: python, xml-rpc

The following piece of code collects links in a Pligg database (but could be any kind of source like RSS feed...) and automatically builds and publishes entries in a blog using XML-RPC.

A small database class :

.. code-block :: python

    class DatabaseAPI(object):
        def connect(self, host="localhost", port=3306, user="root", passwd="root123", db="mysql"):
            import MySQLdb
            self.conn = MySQLdb.connect(host, user, passwd, db)
            
        def disconnect(self):
            self.conn.close()
        
        def fetchall(self, sqlquery):
            cursor = self.conn.cursor()
            cursor.execute(sqlquery)
            return cursor.fetchall()


A Blog publishing class :

.. code-block :: python

    class BlogAPI(object):
        def __init__(self, urlapi, username, password):
            import xmlrpclib
            self.xmlrpclib = xmlrpclib
            try:
                self.server = xmlrpclib.ServerProxy( urlapi )
            except:
                raise Exception( "Could not connect to %s" % url )
            self.username = username
            self.password = password

        def newPost(self, title, description, blogid = '1', publish = True ):
            if description == "":
                description = "<em>empty entry</em>"
            post = {}
            post['title'] = title
            post['description'] = description
            try:
                r = self.server.metaWeblog.newPost( blogid, self.username, self.password, post, publish )
                return r
            except self.xmlrpclib.Fault, fault:
                raise Exception( fault.faultString )

Build the SQL query : all entries of current week

.. code-block :: python

    import datetime
    dt = datetime.timedelta(weeks=-1)
    today = datetime.date.today()
    agelimit = today + dt
    stmt = """
    SELECT link_url, link_url_title
    FROM pligg_links
    WHERE link_status = 'published' AND link_published_date > "%s"
    ORDER BY link_published_date DESC""" % agelimit.strftime("%Y%m%d000000")


Put everything together :

.. code-block :: python

    db = DatabaseAPI()
    db.connect(user="user", passwd="pass", db="name")
    entries = db.fetchall(stmt)
    db.disconnect()

    body = """
    <ul>"""
    for entry in entries:
        body += """
        <li><a href="%s">%s</a></li>""" % (entry[0], entry[1])
    body += """
    </ul>"""

    blog = BlogAPI("http://yourblog/xmlrpc/", "user", "pass")
    title = "Links week #%s" % today.strftime("%W")
    blog.newPost(title, body)



