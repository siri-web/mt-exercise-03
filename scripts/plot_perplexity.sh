#! /bin/bash

scripts=$(dirname "$0")
base=$(realpath $scripts/..)
logs=$base/logs

pip3 install pandas matplotlib

python3 $scripts/plot_perplexity.py \
    --logfiles $logs/log_0.csv $logs/log_0.3.csv $logs/log_0.4.csv $logs/log_0.5.csv $logs/log_0.8.csv \
    --out $logs/validation.csv --type v

python3 scripts/plot_perplexity.py \
    --logfiles $logs/log_0.csv $logs/log_0.3.csv $logs/log_0.4.csv $logs/log_0.5.csv $logs/log_0.8.csv \
    --out $logs/training.csv --type t 

