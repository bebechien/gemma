FROM us-docker.pkg.dev/vertex-ai/training/ray-gpu.2-9.py310:latest

# Install training libraries.
ENV PIP_ROOT_USER_ACTION=ignore
COPY requirements.txt .
RUN pip install -r requirements.txt
