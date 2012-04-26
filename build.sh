#!/bin/bash
virtualenv -q env
source env/bin/activate
#pip install -U pelican
rm -rf output
pelican -v blog.mathieu-leplatre.info -t pelican-theme -s blog.mathieu-leplatre.info/settings.py -o output
deactivate
gnome-open output/index.html
