A very Simple and Stupid plugin system in python
################################################

:tags: python
:date: 2011-09-02


Two convenience functions for listing and importing python modules :

.. code-block :: python

    # utils.py

    import os
    
    def plugins_list(plugins_dirs):
        """ List all python modules in specified plugins folders """
        for path in plugins_dirs.split(os.pathsep):
            for filename in os.listdir(path):
                name, ext = os.path.splitext(filename)
                if ext.endswith(".py"):
                    yield name


    def import_plugins(plugins_dirs, env):
        """ Import modules into specified environment (symbol table) """
        for p in plugins_list(plugins_dirs):
            m = __import__(p, env)
            env[p] = m


And now use ``import_plugins()`` wherever you need to use them !

.. code-block :: python

    # yourapp.py
    
    import os
    from utils import import_plugins
    
    plugins_dirs = "plugins/:module/plugins/"
    sys.path.extend(plugins_dirs.split(os.pathsep))
    
    import_plugins(plugins_dirs, globals())


Note that in order to list all sub-classes of a specific one, you can use `this 
recursive function <http://code.activestate.com/recipes/576949/>`_.

That's all folks !

It is very simple and very stupid, but useful :) You might now want to have
a look at serious stuff like `Yapsy <http://packages.python.org/Yapsy/>`_ or
`PkgResouces <http://packages.python.org/distribute/pkg_resources.html>`_.
