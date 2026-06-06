FROM mcr.microsoft.com/vscode/devcontainers/python:3.12
USER root
RUN apt-get update && apt-get install -y curl git && apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN su vscode -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
ENV PATH="/workspace/.venv/bin:/home/vscode/.local/bin:/home/vscode/.cargo/bin:$PATH"
USER vscode
WORKDIR /workspace
