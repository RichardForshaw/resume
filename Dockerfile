# Amaysim serverless includes:
# node
# python 3.9.7
# yarn
# serverless
FROM amaysim/serverless:3.22.0

# Setup working directory
WORKDIR /opt/project

# Install general python packages
RUN pip3 install --no-cache --upgrade boto3 pytest

# Install MKDocs requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Nnstall nodefiles for SLS
COPY sls/package.json sls/package-lock.json sls/
WORKDIR /opt/project/sls
RUN npm install
WORKDIR /opt/project

# For access to web testing
EXPOSE 8000

ENTRYPOINT bash
