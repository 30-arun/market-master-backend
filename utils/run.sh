sed -i "" "/ssl_certificate_key[[:space:]]*/a\\
ssl_certificate_key /etc/ssl/private/new-example.com.key;\\
" config


echo "server_name olddomain.com;" | sed "s|^\(server_name.*\);|\1 exmple.com www.example.com;|"
