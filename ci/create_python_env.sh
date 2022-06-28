#!/bin/bash
virtualenv -p python3.7 ENV
./ENV/bin/pip install pip --upgrade
./ENV/bin/pip install --use-deprecated=legacy-resolver -r requirements.txt
./ENV/bin/pip install --use-deprecated=legacy-resolver -r test-requirements.txt
