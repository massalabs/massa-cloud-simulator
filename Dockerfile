# Set the version to use
#FROM rustlang/rust:nightly
FROM debian:bullseye-slim

ARG user=user
ARG group_id=2424
ARG user_id=4242
ARG group=docker

#ENV UID=${user_id}
#ENV GID=${group_id}

# Update the machine
RUN apt-get update -y

# Install required packages
RUN apt-get install pkg-config \
                    curl \
                    git \
                    build-essential \
                    python3 \
                    libssl-dev \
                    libclang-dev -y

# Install rustup using curl
#RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -y | sh
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

# Configure the path for rust
#RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc
ENV PATH="/root/.cargo/bin:${PATH}"

# Install nigthly using rustup
RUN rustup toolchain install nightly

# Set nigthly as default
RUN rustup default nightly

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Create the group docker and add the user "user" to the group docker
RUN useradd user -m -u 1001

RUN echo "user:user" | chpasswd

#RUN cargo -help
