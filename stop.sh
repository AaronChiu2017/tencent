#!/usr/bin/env bash

curl http://$1:6800/cancel.json -d project=tencent -d job=$2