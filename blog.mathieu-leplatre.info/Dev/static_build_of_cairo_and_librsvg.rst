Static build of Cairo and librsvg
#################################

:date: 2008-07-01 11:25
:tags: cairo, svg, C

.. image:: images/unicode.png


Why ?
=====
* Convert SVG files to PDF or PNG, with full Unicode support (right-to-left languages), transparency, gradients, PDF image compression, ... 
* Cairo and librsvg are the best in town.
* Cairo and librsvg are very modern libraries which became famous only in the past 3 years. Thus, GNU/Linux distributions do not always have recent versions and full capabilities.
* A `static build` does all the bindings to libraries at compile time, which hence removes specific versions dependencies. *(this method has many drawbacks but can help sometimes)*

The program : svgconvert.c
==========================

  * This program is a merge of Carl Worth's `svg2pdf <http://cgit.freedesktop.org/~cworth/svg2pdf/>`_ and `svg2png <http://cgit.freedesktop.org/~cworth/svg2png/>`_

.. code-block :: c

    /* 
    * Copyright © 2005 Red Hat, Inc.
    * Copyright © 2006 Red Hat, Inc.
    * Copyright © 2007 Red Hat, Inc.
    *
    * Permission is hereby granted, free of charge, to any person
    * obtaining a copy of this software and associated documentation
    * files (the "Software"), to deal in the Software without
    * restriction, including without limitation the rights to use, copy,
    * modify, merge, publish, distribute, sublicense, and/or sell copies
    * of the Software, and to permit persons to whom the Software is
    * furnished to do so, subject to the following conditions:
    *
    * The above copyright notice and this permission notice shall be
    * included in all copies or substantial portions of the Software.
    *
    * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
    * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
    * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    * SOFTWARE.
    *
    * Authors: Kristian Høgsberg <krh@redhat.com>
    * Carl Worth <cworth@redhat.com>
    * Behdad Esfahbod <besfahbo@redhat.com>
    * Mathieu Leplatre <contact@mathieu-leplatre.info>
    */

    #include <stdio.h>
    #include <stdlib.h>
    #include <glib/gprintf.h>
    #include <librsvg/rsvg.h>
    #include <librsvg/rsvg-cairo.h>

    #include <cairo-pdf.h>

    #define FAIL(msg) \
    do { fprintf (stderr, "FAIL: %s\n", msg); exit (-1); } while (0)

    #define PIXELS_PER_POINT 1

    #define PDF 0
    #define PNG 1

    int main (int argc, char *argv[])
    {
        GError *error = NULL;
        RsvgHandle *handle;
        RsvgDimensionData dim;
        double width, height;
        const char *filename = argv[1];
        const char *output_filename = argv[2];
        cairo_surface_t *surface;
        cairo_t *cr;
        cairo_status_t status;
        int mode;

        if (argc != 3)
            FAIL ("usage: svgconvert input_file.svg output_file");

        mode = PDF;
        if (g_str_has_suffix (g_ascii_strdown (output_filename, -1), ".png")) {
            mode = PNG;
        }

        g_type_init ();

        rsvg_set_default_dpi (72.0);
        handle = rsvg_handle_new_from_file (filename, &error);
        if (error != NULL)
            FAIL (error->message);

        rsvg_handle_get_dimensions (handle, &dim);
        width = dim.width;
        height = dim.height;

        if (mode == PNG) {
            surface = cairo_image_surface_create (CAIRO_FORMAT_ARGB32, width, height);
        }
        else {
            surface = cairo_pdf_surface_create (output_filename, width, height);
        }

        cr = cairo_create (surface);

        rsvg_handle_render_cairo (handle, cr);

        status = cairo_status (cr);
        if (status)
            FAIL (cairo_status_to_string (status));

        if (mode == PNG) {
            cairo_surface_write_to_png (surface, output_filename);
        }

        cairo_destroy (cr);
        cairo_surface_destroy (surface);

        return 0;
    }


Build with shared librairies
============================

You would just do :

.. code-block :: bash

    gcc `pkg-config --cflags --libs librsvg-2.0 cairo-pdf` -o svgconvert svgconvert.c


which creates a binary of 9.0K.

Build with static librairies
============================

* First install the development versions of the packages, to make sure you have all **/usr/lib/*.a** mentioned below.
* Use this Makefile, which creates a binary of 5.9M. It was tested on Ubuntu 8.04 which comes with Gnome 2.22, librsvg 2.22 and Cairo 1.6.0.

.. code-block :: bash

    ALL=svgconvert

    MYCFLAGS=`pkg-config --cflags librsvg-2.0 cairo-pdf`
    LDFLAGS=`pkg-config --libs librsvg-2.0 cairo-pdf freetype2 fontconfig pango pangoft2 pangocairo  cairo-ft libthai datrie libgsf-1 gnome-vfs-2.0 libcroco-0.6 libpcre pixman-1 libpng libxml-2.0`
    MYLDFLAGS=$(LDFLAGS) /usr/lib/libgio-2.0.a  /usr/lib/libglib-2.0.a /usr/lib/libselinux.a /usr/lib/libexpat.a /usr/lib/libfreetype.a /usr/lib/libbz2.a /usr/lib/libjpeg.a /usr/lib/libtiff.a /usr/lib/libbz2.a /usr/lib/libz.a /usr/lib/libm.a

    all: $(ALL)

    %: %.c
        $(CC) $^ -pthread $(MYCFLAGS) -static $(MYLDFLAGS) -o $@

    clean:
        rm -f $(ALL) *.o

* To check if **pkg-config** knows about a specific library :

.. code-block :: bash

    $ pkg-config --list-all | grep vfs
    gnome-vfs-sharp-2.0           GnomeVfs - GnomeVfs
    gnome-vfs-2.0                 gnome-vfs - The GNOME virtual file-system libraries
    gnome-vfsmm-2.6               gnome-vfsmm - C++ wrapper for gnome-vfs
    gnome-vfs-module-2.0          gnome-vfs-module - The GNOME virtual file-system module include info

* To check if a library has a specific symbol, use the **nm** command :

.. code-block :: bash

    $ nm /usr/lib/libexpat.a | grep XML_SetStart
    000001c0 T XML_SetStartCdataSectionHandler
    00000240 T XML_SetStartDoctypeDeclHandler
    00000150 T XML_SetStartElementHandler
    000002a0 T XML_SetStartNamespaceDeclHandler


Download
========

* `Source <http://mathieu-leplatre.info/media/svgconvert-src.tar.gz>`_
* `Binary <http://mathieu-leplatre.info/media/svgconvert-bin.tar.gz>`_

References
==========
* `<http://cairographics.org>`_
* `<http://librsvg.sourceforge.net>`_
* Thanks for the precious help of `Carl Worth <http://www.cworth.org>`_ on `#cairo` at irc.freenode.net, Zugzwang and nvteighen on `<http://ubuntuforums.org>`_
