Ajouter un sélecteur de couches (layer switcher) à polymaps
###########################################################

:date: 2011-03-09 12:03
:tags: polymaps, tips, javascript, gis
:lang: fr


Je fais partie de ceux qui sont persuadés que `polymaps <http://polymaps.org/>`_ est tout à fait mature ! 
Certes, il ne fournit pas autant de fonctionnalités et de connecteurs qu'OpenLayers, 
mais il ne semble pas que ce soit son objectif ! Il est léger et personnalisable à souhait !

Pour le prouver, nous allons créer ici un sélecteur de couches pour polymaps.

Javascript n'est pas mon langage de prédilection, encore moins pour faire 
de la programmation orientée objets.

Voici ce que j'ai réussi à comprendre de l'héritage et la portée dans le modèle objet de polymaps :

.. code-block :: javascript

    (function(po) {
      po.classname = function(args) {
       var self = {},      // new class or inheritance
            member;         // member variable
     
        function privatemethod () {
            // [...]
        }

        self.classmethod = function (args) {
            // [...]
            return self;  // allows to chain method calls
        }
     
        return self;
      };
    })(org.polymaps);


Pour faire ce sélecteur de couches, nous aurons besoin d'une classe disposant :

* de variables membres qui stockent la liste de couches disponibles (``layers``) et la couche actuelle (``current``)
* d'une méthode de classe qui bascule d'une couche à l'autre

.. code-block :: javascript

    self.switchto = function (name) {
        var l = layers[name];  // find layer by name
        if (l.map()) {       
           l.visible(true);   // if already loaded, make it visible
        }
        else {
            map.add(l);        // else load it
        }
        if (current) current.visible(false);  // hide current
        current = l;
    }

* d'une méthode qui crée l'interface avec les radio buttons et qui les relie à la méthode précedente

.. code-block :: javascript

    self.container = function (elt) {
        var list = document.createElement('div');
        // [...]
        // For each layer, create a <input>
        for (name in layers) {
            var input = document.createElement('input');
            input.setAttribute('type', 'radio');
            input.setAttribute('value', name);
            // [...]          
            // Link onChange event on radio
            input.onchange = function () {
                self.switchto(this.getAttribute('value'));
            };
            // [...]
            list.appendChild(input);
        }
        // [...]
        elt.appendChild(list);
        return self;
    }

Maintenant il suffit de l'utiliser ! Voici un exemple simple avec deux couches :

.. code-block :: javascript

    // Create a normal map
    map = po.mcmap()
            .container(document.getElementById("map").appendChild(po.svg("svg")))
            .add(po.interact());
     
    // Define the layers
    var layers = {
        "layer1" :
        po.image()
          .url(po.url("http://server1/{Z}/{X}/{Y}.png"))
          .id('l1'),
     
        "layer2" :
        po.image()
          .url(po.url("http://server2/{Z}/{X}/{Y}.png"))
          .id('l2'),
    };
     
    // Add the default one
    map.add(layers["layer1"]);
     
    // Create the switcher
    po.switcher(map, layers, {title : 'Fond de carte'})
      .container(document.getElementById("layerswitcher"));

Et voilà ! Nous avons notre sélecteur de couches, avec un code html 
tout simple (``div``, ``input``, ``label``), facile à styler en CSS, 
contrairement au `gros pavé généré par le *LayerSwitcher* d'OpenLayers <http://pastebin.com/LQPBv6tZ>`_.

.. image:: images/polymaps-switcher.png


Pour accéder au code complet et l'améliorer : "`Fork me on GitHub <https://github.com/makinacorpus/polymaps-extensions>`_" ! 

*Article original publié chez* `Makina Corpus <http://www.makina-corpus.org/blog/ajouter-un-s%C3%A9lecteur-de-couches-layer-switcher-%C3%A0-polymaps>`_
