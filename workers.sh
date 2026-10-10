#!/bin/bash
celery -A config worker -l info --concurrency=2