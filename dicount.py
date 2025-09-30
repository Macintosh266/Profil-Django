
# 1-Qadam
# [Unit]
# Description=gunicorn socket

# [Socket]
# ListenStream=/run/gunicorn.sock

# [Install]
# WantedBy=sockets.target


# 2-Qadam

# [Unit]
# Description=gunicorn daemon
# Requires=gunicorn.socket
# After=network.target

# [Service]
# User=root
# Group=www-data
# WorkingDirectory=/var/www/Profil-Django
# ExecStart=/var/www/Profil-Django/venv/bin/gunicorn \
#           --access-logfile - \
#           --workers 3 \
#           --bind unix:/run/gunicorn.sock \
#           config.wsgi:application

# [Install]
# WantedBy=multi-user.target

# 3-Qadam

# server {
#     listen 80;
#     server_name 46.101.203.157 ;

#     location = /favicon.ico { access_log off; log_not_found off; }
#     location /static/ {
#         root /var/www/Profil-Django;
#     }

#     location / {
#         include proxy_params;
#         proxy_pass http://unix:/run/gunicorn.sock;
#     }
# }