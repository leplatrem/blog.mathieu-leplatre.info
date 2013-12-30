Text extents with Python Cairo
##############################

:date: 2009-08-10 10:20
:tags: cairo, python

I needed this and could not find it. So I share it here (and even better if Google'd index it!)

.. code-block :: python

    def textwidth(text, fontsize=14):
        try:
            import cairo
        except Exception, e:
            return len(str) * fontsize
        surface = cairo.SVGSurface('undefined.svg', 1280, 200)
        cr = cairo.Context(surface)
        cr.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(fontsize)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
        return width




