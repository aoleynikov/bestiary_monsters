#!/usr/bin/env bash
docker-compose build web && docker-compose run web nosetests
