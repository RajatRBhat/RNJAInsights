# Use the official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app


# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container's working directory
COPY . .

# Run as non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app USER appuser

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run your Streamlit application
CMD ["streamlit", "run", "run_app.py", "--server.port=8501", "--server.address=0.0.0.0"]