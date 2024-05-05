Tested using Ubuntu 20.04.


1. apt install apache2

2. cd /var/www/

3. git clone https://github.com/AganFebro/flask-web.git

4. mv flask-web/ flaskweb

5. cd flaskweb

6. mkdir logs

7. touch logs/error.log

8. touch logs/access.log

9. apt install pipenv

10. pip install flask flask_sqlalchemy flask_login

11. apt install libapache2-mod-wsgi-py3

12. cp flask.conf /etc/apache2/sites-available/

13. nano /etc/apache2/sites-available/flask.conf
#Bagian ServerName isi IP VPS mu! Lalu save (Ctrl+O) dan exit (Ctrl+X)

14. a2ensite flask.conf

15. systemctl reload apache2

LOG ERROR berada di /var/www/flaskweb/logs/error.log
