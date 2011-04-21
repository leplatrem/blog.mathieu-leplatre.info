virtualenv -q env
pip install -U pelican
source env/bin/activate
rm -rf output
pelican blog.mathieu-leplatre.info -t pelican-theme -s blog.mathieu-leplatre.info/settings.py
firefox output/index.html
