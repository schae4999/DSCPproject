#!/bin/bash
set -e
tar -xzf metadata.tar.gz
python3 model.py CodeNet_subset/metadata
