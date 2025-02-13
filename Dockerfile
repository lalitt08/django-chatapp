FROM ubuntu:18.04

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev \
    default-libmysqlclient-dev build-essential git \
    libpq-dev  # <== Add this line

# Clone the repository
RUN git clone https://${ACCESS_TOKEN}@github.com/lalitt08/django-chatapp.git /app

WORKDIR /app

# Install Python dependencies
RUN pip3 install virtualenv && \
    virtualenv -p /usr/bin/python3 venv && \
    . venv/bin/activate && \
    pip3 install -r requirements.txt && \
    pip3 install mysqlclient

# Run Django migrations and start the server
CMD ["/bin/bash", "-c", "source venv/bin/activate && python3 /app/fundoo/manage.py makemigrations && python3 /app/fundoo/manage.py migrate && python3 /app/fundoo/manage.py runserver 0.0.0.0:8000"]

EXPOSE 8000
