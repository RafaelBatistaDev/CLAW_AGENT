# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Instalar Rust (versão stable)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    . ${HOME}/.cargo/env && \
    rustup component add rustfmt clippy

# Instalar Python e ferramentas de development
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip e instalar ferramentas Python comuns
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install \
    pytest \
    black \
    pylint \
    mypy

# Criar diretórios necessários
RUN mkdir -p /home/claw/.claw/{config,logs,cache}

WORKDIR /workspace

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD cargo --version && python3 --version && git --version || exit 1

CMD ["/bin/bash"]
