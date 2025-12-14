#!/bin/bash
set -e
echo "Generating dataset from Ephect source..."
python lora-php-ephect/scripts/generate_dataset.py
echo "Starting training..."
accelerate launch --config_file accelerate.yaml lora-php-ephect/train.py
