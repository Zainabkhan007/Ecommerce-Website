FROM python:3.10-slim

# Install SQLite 3.31 or later
RUN apt-get update && \
    apt-get install -y sqlite3 libsqlite3-dev && \
    sqlite3 --version  # Verify the installed version

# Set the working directory
WORKDIR /eccomerce

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]