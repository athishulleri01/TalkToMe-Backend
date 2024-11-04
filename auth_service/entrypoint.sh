#!/bin/bash

# Start the Django application
gunicorn -c auth/gunicorn_config.py auth.wsgi:application
