#!/bin/bash
set -e

problem_id="$1"

tar -xzf "${problem_id}.tar.gz"

python3 extract_features.py "$problem_id"