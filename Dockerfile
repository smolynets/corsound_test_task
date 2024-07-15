FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# # Base image from NVIDIA
# FROM nvcr.io/nvidia/pytorch:22.12-py3

# # Install necessary packages
# RUN apt-get update && apt-get install -y \
#     curl \
#     gnupg \
#     && rm -rf /var/lib/apt/lists/*

# # Set up the NVIDIA Container Toolkit repository and install the NVIDIA Container Toolkit
# RUN distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
#     && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add - \
#     && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list \
#     && apt-get update \
#     && apt-get install -y nvidia-container-toolkit \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Verify the NVIDIA installation
# RUN nvidia-smi

# # Install additional dependencies for your application
# RUN apt-get update && apt-get install -y \
#     python3-pip \
#     && pip3 install --no-cache-dir \
#     fastapi \
#     uvicorn \
#     transformers \
#     pillow \
#     torch \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Copy your application code to the container
# COPY . /app

# # Set the working directory
# WORKDIR /app

# # Command to run the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
