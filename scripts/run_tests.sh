#!/usr/bin/env bash
docker-compose build monsters && docker-compose run monsters nosetests
