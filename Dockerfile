# Amaysim serverless includes:
# node
# python 3.9.7
# yarn
# serverless
FROM amaysim/serverless:3.39.0

# Setup working directory
WORKDIR /opt/project

# Bypasses the externally managed environment restriction (OK in dockerfile)
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# upgrade pip3
RUN python3 -m pip install --no-cache --upgrade pip

# Install general python packages
RUN pip3 install --no-cache --upgrade boto3 pytest

# Install MKDocs requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install node for Claude
RUN apk add --no-cache nodejs npm

# Install nodefiles for SLS
COPY sls/package.json sls/package-lock.json sls/
WORKDIR /opt/project/sls
RUN npm install
WORKDIR /opt/project

# Set env variable for default AWS profile
ENV AWS_PROFILE=raf-tech

# For access to web testing
EXPOSE 8000

ENTRYPOINT bash
