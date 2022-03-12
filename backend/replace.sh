#!/bin/sh

sed "s/href=\"\/dist\/index.css\"/href=\"{{ url_for(\'static\', path=\'\/dist\/index.css\') }}\"/g" ../backend/static/index.html > tmp.txt
\cp -f tmp.txt ../backend/static/index.html
rm tmp.txt
sed "s/src=\"\/dist\/index.js\"/src=\"{{ url_for(\'static\', path=\'\/dist\/index.js\') }}\"/g" ../backend/static/index.html > tmp.txt
\cp -f tmp.txt ../backend/static/index.html
rm tmp.txt
sed "s/src=\"\/favicon.ico\"/src=\"{{ url_for(\'static\', path=\'\/favicon.ico\') }}\"/g" ../backend/static/index.html > tmp.txt
\cp -f tmp.txt ../backend/static/index.html
rm tmp.txt