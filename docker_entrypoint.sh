#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run the Streamlit app
exec streamlit run /docker_app/app/main.py --server.port 8501 --server.address 0.0.0.0