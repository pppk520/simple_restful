from flask.ext.cache import Cache                                               
                                                                                
cache = Cache(config={'CACHE_TYPE': 'simple',
                      'CACHE_DEFAULT_TIMEOUT': 600,
                      'CACHE_THRESHOLD': 1000}) 

