FROM python:3.11.5 AS base

FROM base AS builder
# System packages
RUN apt-get update && apt-get install --no-install-recommends cmake nano -y
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /astrazeneca

# 1 - copy source files
COPY . .

# 2 - install poetry
RUN pip3 install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root
RUN poetry cache clear --all . -n

ENTRYPOINT ["poetry", "run", "python", "main.py"]
