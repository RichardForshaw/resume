# Amaysim serverless includes:
# node
# python 3.9.7
# yarn
# serverless
FROM amaysim/serverless:3.10.2

# Install python packages
RUN pip3 install --no-cache --upgrade \
	boto3  \
    mkdocs

# For access to web testing
EXPOSE 8000

# Setup working directory
WORKDIR /opt/project

ENTRYPOINT bash
