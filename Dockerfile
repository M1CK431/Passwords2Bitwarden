FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Create an output directory for the converted files
RUN mkdir -p /app/output

# Copy the current directory contents into the container at /app
COPY . /app

# Make sure the main script is executable
RUN chmod +x main.py

# Default command for running the script, accepts zip file and output directory as arguments
ENTRYPOINT ["python", "./main.py"]
CMD ["/app/archive.zip", "/app/output"]
