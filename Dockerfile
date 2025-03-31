# Use Python 3.12 official image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Set environment variables to avoid permission errors with Hugging Face cache
ENV HF_HOME=/app/.cache

# Create the cache directory with proper permissions
RUN mkdir -p /app/.cache && chmod -R 777 /app/.cache

# Create the uploads directories with full permissions
RUN mkdir -p /app/data/uploads/resumes /app/data/uploads/job_descriptions && chmod -R 777 /app/data

# Create the parent models directory with full permissions and correct ownership
RUN mkdir -p /app/models/summarization_model && \
    chmod -R 777 /app/models/summarization_model && \
    chown -R 1000:1000 /app/models


# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . /app

# Command to run the application using Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860"]
