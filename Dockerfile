# Use Python 3.12 official image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Set environment variables to avoid permission errors with Hugging Face cache
ENV HF_HOME=/app/.cache

# Create the cache directory
RUN mkdir -p /app/.cache && chmod -R 777 /app/.cache

# Copy the requirements file and install dependencies
COPY requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY ..

# Command to run the application using Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860"]