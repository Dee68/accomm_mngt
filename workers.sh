#!/bin/bash
celery -A accomm_mngmt worker -l info --concurrency=2