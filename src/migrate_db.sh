./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic --no-input -i sass

./manage.py loaddata college/fixtures/*.*
./manage.py loaddata educationpart/fixtures/*.*
./manage.py loaddata schedule/fixtures/*.*

./manage runserver