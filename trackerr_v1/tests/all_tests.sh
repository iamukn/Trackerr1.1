#!/usr/bin/bash
echo '!!CHECKING FOR TESTS IN THE BUSINESS OWNER APP ;)!!! ;)'
../manage.py test ../business/tests/
echo 'CHECKING FOR TESTS IN THE LOGISTICS PARTNER APP ;)'
../manage.py test ../logistics/tests/
echo 'CHECKING FOR TESTS IN THE USER APP!!! ;)'
../manage.py test ../user/tests/
echo 'CHECKING FOR TESTS IN THE Authetication APP!!! ;)'
../manage.py test ../authentication/tests/
echo 'CHECKING FOR TESTS IN THE Tracking APP!!! ;)'
../manage.py test ../tracking_information/tests/
