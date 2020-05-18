#!/bin/bash


cd /usr/share/redmine/app

rails server webrick -e production -b 0.0.0.0

