FROM httpd:2.4

# Python + lo necesario para compilar mod_wsgi contra este Apache
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-venv python3-dev gcc libapr1-dev libaprutil1-dev \
    && rm -rf /var/lib/apt/lists/*

# virtualenv con mod_wsgi, flask y pymongo
RUN python3 -m venv /opt/venv
COPY requirements.txt /app/requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# registrar el modulo wsgi y nuestro VirtualHost en httpd.conf
RUN /opt/venv/bin/mod_wsgi-express module-config >> /usr/local/apache2/conf/httpd.conf \
    && echo "Include conf/extra/libros.conf" >> /usr/local/apache2/conf/httpd.conf
COPY apache-libros.conf /usr/local/apache2/conf/extra/libros.conf

# codigo de la app
COPY app.py app.wsgi /app/

# CMD (httpd-foreground) y EXPOSE 80 se heredan de httpd:2.4
