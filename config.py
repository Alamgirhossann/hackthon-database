import os

API_CONFIG_ELASTICSEARCH_URL_WITH_USER_PASS = os.getenv(
    "API_CONFIG_ELASTICSEARCH_URL_WITH_USER_PASS",
    "https://analystt:Hello!1234@search-analystt-search-rzs6ykgi7pz7lxarr7eafmgapy.ap-south-1.es.amazonaws.com",
)

API_CONFIG_DEFAULT_USERNAME = os.getenv("API_CONFIG_DEFAULT_USERNAME", "analystt")
API_CONFIG_DEFAULT_PASSWORD = os.getenv("API_CONFIG_DEFAULT_PASSWORD", "Hello!1234")

