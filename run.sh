#!/usr/bin/env bash

curl http://10.211.55.4:6800/schedule.json -d project=tencent -d spider=zhaopin
curl http://127.0.0.1:6800/schedule.json -d project=tencent -d spider=zhaopin