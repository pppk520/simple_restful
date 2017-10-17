## Simple RESTful Web Service Demo                                              
### Nginx + Flask + uWSGI + flasgger                                                    

## Docker Run                                                                      
```bash                                                                         
sudo make build                                                                 
sudo make test
sudo make run HOST_PORT=[your_port]                                             
```

Access apidocs from:
```                                                                               
http://[you_server]:[your_port]/apidocs                                         
``` 

#### [NGINX](https://www.nginx.com/resources/wiki/)
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server. NGINX is known for its high performance, stability, rich feature set, simple configuration, and low resource consumption.

#### [Flask](http://flask.pocoo.org/)
Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions. And before you ask: It's BSD licensed!

#### [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/)
uWSGI is a deployment option on servers like nginx, lighttpd, and cherokee; see FastCGI and Standalone WSGI Containers for other options. To use your WSGI application with uWSGI protocol you will need a uWSGI server first. uWSGI is both a protocol and an application server; the application server can serve uWSGI, FastCGI, and HTTP protocols.

#### [flasgger](https://github.com/rochacbruno/flasgger)
Flasgger is a Flask extension to extract OpenAPI=Specification from all Flask views registered in your API.

Flasgger also comes with SwaggerUI embedded so you can access http://localhost:5000/apidocs and visualize and interact with your API resources.

Flasgger also provides validation of the incoming data, using the same specification it can validates if the data received as as a POST, PUT, PATCH is valid against the schema defined using YAML, Python dictionaries or Marshmallow Schemas.

[OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md)



