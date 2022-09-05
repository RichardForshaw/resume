# Amaysim serverless includes:
# node
# python 3.9.7
# yarn
# serverless
FROM amaysim/serverless:3.10.2

# Setup working directory
WORKDIR /opt/project

# Install general python packages
RUN pip3 install --no-cache --upgrade boto3

# Install MKDocs requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# For access to web testing
EXPOSE 8000

ENTRYPOINT bash
