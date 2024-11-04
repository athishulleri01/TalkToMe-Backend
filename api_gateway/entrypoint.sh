#!/bin/bash

# Start the Django application
gunicorn -c api_gateway/gunicorn_config.py api_gateway.wsgi:application
