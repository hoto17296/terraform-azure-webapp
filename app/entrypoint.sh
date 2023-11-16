#!/bin/bash -eu

service ssh start

exec "$@"