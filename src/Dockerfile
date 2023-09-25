# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Suggest that users mount a volume at /app/data
VOLUME /app/datafiles

# Define environment variable
ENV DB_URL postgresql://postgres:example@db/postgres
ENV FLASK_APP="app.py"

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]