#!/usr/bin/bash
echo '!!CHECKING FOR TESTS IN THE BUSINESS OWNER APP ;)!!! ;)'
../manage.py test ../business/tests/
echo 'CHECKING FOR TESTS IN THE LOGISTICS PARTNER APP ;)'
../manage.py test ../logistics/tests/
echo 'CHECKING FOR TESTS IN THE USER APP!!! ;)'
../manage.py test ../user/tests/
