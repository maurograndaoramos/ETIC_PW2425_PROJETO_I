# Base image
FROM <base_image>

# Set the working directory
WORKDIR /app

# Copy the source code to the working directory
COPY . .

# Install dependencies (if any)
RUN <command_to_install_dependencies>

# Expose a port (if needed)
EXPOSE 

# Define the command to run the application
CMD <command_to_run_application>