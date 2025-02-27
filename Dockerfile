FROM python:3.9.13

# Set non-interactive mode for apt-get
ARG DEBIAN_FRONTEND=noninteractive

# Create and set the working directory to /docker_app (non-root)
RUN mkdir -p /docker_app
WORKDIR /docker_app

# Copy the entire local directory to /docker_app in the container
COPY . /docker_app

# Make Python scripts in /docker_app executable
RUN chmod +x /docker_app/app/*.py

# Update package lists
RUN apt-get update && echo "Updated package lists" || (echo "Failed to update package lists" && exit 1)

# Install required packages one by one for better error handling
RUN apt-get install -y --no-install-recommends unixodbc && echo "Installed unixodbc" || (echo "Failed to install unixodbc" && exit 1)
RUN apt-get install -y --no-install-recommends unixodbc-dev && echo "Installed unixodbc-dev" || (echo "Failed to install unixodbc-dev" && exit 1)
RUN apt-get install -y --no-install-recommends freetds-dev && echo "Installed freetds-dev" || (echo "Failed to install freetds-dev" && exit 1)
RUN apt-get install -y --no-install-recommends freetds-bin && echo "Installed freetds-bin" || (echo "Failed to install freetds-bin" && exit 1)
RUN apt-get install -y --no-install-recommends tdsodbc && echo "Installed tdsodbc" || (echo "Failed to install tdsodbc" && exit 1)
RUN apt-get install -y --no-install-recommends build-essential && echo "Installed build-essential" || (echo "Failed to install build-essential" && exit 1)

# Clean up to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies from requirements.txt
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Expose the Streamlit port 8501
EXPOSE 8501

# Ensure the entrypoint script is executable
RUN chmod +x /docker_app/docker_entrypoint.sh

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["./docker_entrypoint.sh"]
