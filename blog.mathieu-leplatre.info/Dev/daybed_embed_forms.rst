Embed Daybed forms
##################

:date: 2013-07-23 14:25
:tags: daybed, javascript, backbone
:lang: en


A brief article to introduce `backbone-daybed <https://github.com/spiral-project/backbone-daybed>`_, a few
helpers to render Web forms for Daybed models.


.. image :: http://upload.wikimedia.org/wikipedia/commons/7/70/Antikes_Sofa_Diwan_furniert_Laden_daybed.jpg
    :alt: Antikes Sofa Diwan furniert Laden daybed
    :width: 512


=========================
Daybed, lay down and REST
=========================

`Daybed <https://github.com/spiral-project/daybed>`_ is a data validation and storage API, written in Python,
using Pyramid and the fantastic `Cornice <https://cornice.readthedocs.org/>`_ addon.

It's a minimalist Web API where you :

* define models (schemas)
* validate data and store data
* retrieve and update records

Key features are:

* `CORS <http://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`_ built-in support
* pluggable datastore engines (default is *CouchDB*)
* Geometry fields (maps!)
* `Spore <https://github.com/SPORE/specifications>`_
* Access Control (*under development*)

It's a side-project we've been hacking on for a while, and we envision `many
applications <https://github.com/spiral-project/daybed/wiki/Use-cases>`_ !
One of them is, since the beginning, a Web forms service !


================
Models are yours
================

In order to create your own models, you can either use the
crude GUI of `daybed-maps <http://leplatrem.github.io/daybed-map/>`_ 
**or** post a JSON manually on the `Daybed instance <http://daybed.lolnet.org>`_ we run for you.

In both cases you will reference your model definition using 
the ``ìd`` you chose.

Below, we define ``demo-poll-conf`` using cUrl in the command-line.

The model will be a stupid poll to ask how many conferences you attended
in the past year.

.. code-block :: bash

    # in a terminal...
    definition='{
    "title": "Conferences Poll",
    "description": "How many conferences attended last year ?",
    "fields": [
      {
        "name": "total",
        "type": "int",
        "description": "How many times ?"
      }, {
        "name": "category",
        "type": "enum",
        "choices": ["Web", "Strategy", "Technology"],
        "description": "Mostly in..."
      }
    ]}'

    curl -XPUT http://daybed.lolnet.org/definitions/demo-poll-conf -d "${definition}"


==================================
backbone-daybed, simple and stupid
==================================

Backbone.js is not the *next* big thing :) *#ooold, it's sooo 2011* !

But frankly, it has remained simple, very easy to learn and yet quite efficient!
That's why I chose it to demo the power of having storage-as-a-service with Daybed.
Plus, `backbone-forms <https://github.com/powmedia/backbone-forms>`_ provided
the right level of abstraction I needed !

For example, here we embed a form in the page for the model we just created, 
and start polling the audience !

The few lines of Javascript below render the form and reacts on submission !

.. code-block :: html

    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.4.2/underscore-min.js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.0.0/backbone-min.js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/mustache.js/0.7.0/mustache.min.js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/backbone-forms/0.12.0/backbone-forms.min.js"></script>
    <script type="text/javascript" src="https://rawgithub.com/spiral-project/backbone-daybed/1e410a85/backbone-daybed.js"></script>
    <script type="text/javascript">

        var form = Daybed.renderForm('#demo-form-container', {id: 'demo-poll-conf'});

        form.on('created', function (record) {
            // plot chart !
        })
    </script>

.. raw :: html

    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.4.2/underscore-min.js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.0.0/backbone-min.js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/mustache.js/0.7.0/mustache.min.js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/backbone-forms/0.12.0/backbone-forms.min.js"></script>
    <script type="text/javascript" src="https://rawgithub.com/spiral-project/backbone-daybed/1e410a85/backbone-daybed.js"></script>
    <script type="text/javascript" src="https://rawgithub.com/nnnick/Chart.js/master/Chart.min.js"></script>
    <style>
        #demo-form-container {
            border: 1px solid #6C0AAB;
            margin-bottom: 30px;
            display: inline-block;
            padding: 10px;
            border-radius: 5px;
        }
        #demo-form-container .field-error {
            color: red;
        }
        #demo-form-container label {
            font-weight: bold;
        }
        #demo-form-container ul {
            margin: 0px;
            list-style-type: none;
        }
        #demo-form-container a.btn {
            float: right;
            text-decoration: none;
            background-color: #6C0AAB;
            color: white;
            border-radius: 3px;
            font-size: 16px;
        }
    </style>
    <div id="demo-form-container"></div>

    <script type="text/javascript">
        $(document).ready(function () {
            Daybed.SETTINGS.SERVER = "http://daybed.lolnet.org";  // no trailing slash

            var form = Daybed.renderForm('#demo-form-container',
                                         {id: 'demo-poll-conf',
                                          title: 'Conferences poll :',
                                          save: 'Submit',
                                          cancel: null});

            // Fetch all the records
            var records = new Daybed.ItemList(form.definition);
            records.fetch();

            // On submission, plot the chart
            form.on('created', function (record) {
                records.add(record);

                // Prepare plot data
                var data = {
                    labels : [],
                    datasets : [{
                        fillColor : "#E0E4CC",
                        strokeColor : "#6C0AAB",
                        data : []
                    }]
                };
                var byCat = {};
                records.each(function (r) {
                    var cat = r.attributes.category;
                    if (!byCat[cat]) byCat[cat] = [];
                    byCat[cat].push(r.attributes.total);
                });
                for(var cat in byCat) {
                    var sum = _.reduce(byCat[cat], function(memo, num){ return memo + num; }, 0),
                        val = sum / byCat[cat].length;
                    data.labels.push(cat);
                    data.datasets[0].data.push(val);
                }

                // Render the bar chart
                var ctx =  $('#demo-form-container').html('<p>Avg. per category</p>'+
                                                          '<canvas height="200"/>')
                                                    .find('canvas')[0].getContext("2d"),
                    chart = new Chart(ctx).Bar(data);
            });
        });
    </script>


The helper downloads the definition JSON, renders fields within an HTML form with
*backbone-forms*. And in this example specifically, on submission, we fetch all the records, 
compute average values by category in order to plot some naive chart using `Chart.js <http://chartjs.org>`_.

.. image:: /images/backbone-daybed-preview.png
    :width: 700

You can also have a look at the very few lines of the backbone-daybed demo, it's dead easy !
It features a CRUD application : Create, edit and delete records for the model of your choice ! http://spiral-project.github.io/backbone-daybed/#demo-poll-conf (*See URL hash*)


=======
Shortly
=======

* Daybed is a generic backend where you define models, validate and post data ;
* There are already `various working applications <https://github.com/spiral-project/daybed/wiki/Use-cases>`_ built with this storage-as-a-service ;
* Most Javascript frameworks will play well natively with Daybed REST API ;
* backbone-daybed is just a helper to render Daybed models as forms, .... `and a little bit more <https://github.com/spiral-project/backbone-daybed/#readme>`_ !


So far, Daybed data is not protected (like a wiki), but access control is currently being implemented :)

Stay tuned !
