import os

RABBITMQ = {
    'USERNAME': os.getenv("RABBIT_USERNAME", "admin"),
    'PASSWORD': os.getenv("RABBIT_PASSWORD", "admin"),
    'HOST': os.getenv("RABBIT_HOST", "localhost")
}

FULLTEXT_SEARCH = {
    'BASE_URL': os.getenv('FDK_FULLTEXT_SEARCH_BASE_URL', 'http://localhost:5000')
}

LOGGING = {
    'LEVEL': os.getenv('LOG_LEVEL', 'INFO')
}
