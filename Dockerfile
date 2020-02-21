# Amaysim serverless includes:
# node
# python 3.7.5
# yarn
# serverless
FROM amaysim/serverless:1.60.0

# Install python packages
RUN pip3 install --no-cache --upgrade \
	boto3

# For access to web testing
EXPOSE 8000

# Setup working directory
WORKDIR /opt/project

ENTRYPOINT bash
