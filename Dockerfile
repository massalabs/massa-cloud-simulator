# Builder Image
FROM debian:bullseye-slim AS builder

ARG GIT_REPO=https://github.com/massalabs/massa

# Update the machine
RUN apt-get update -y

# Upgrade the machine
RUN apt-get upgrade -y

# Install required packages
RUN apt-get install pkg-config \
                    curl \
                    git \
                    build-essential \
                    python3 \
                    libclang-dev -y

# Install rustup using curl
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

# Configure the path for rust
ENV PATH="/root/.cargo/bin:${PATH}"

# Install nigthly using rustup
RUN rustup toolchain install nightly

# Set nigthly as default
RUN rustup default nightly

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Create the user user
RUN useradd user -m -u 1001

# Set the username user and the password user
RUN echo "user:user" | chpasswd

# Clone the repository
RUN git clone ${GIT_REPO}

RUN cargo build --release --bin massa-node --bin massa-client 

WORKDIR /massa


############# RUNTIME #############

# Production Image
FROM debian:bullseye-slim AS runtime

ARG GIT_REPO=https://github.com/massalabs/massa

# Update the machine
RUN apt-get update -y

# Install required packages
RUN apt-get install python3 \
                    git -y

# Upgrade the machine
RUN apt-get upgrade -y

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Create the user user
RUN useradd user -m -u 1001

# Set the username user and the password user
RUN echo "user:user" | chpasswd

# Clone the repository
RUN git clone ${GIT_REPO}

WORKDIR /massa

# To Fix :
#COPY --from=builder /massa-client/config /source/massa-client/config
#COPY --from=builder /massa-client/base_config /source/massa-client/base_config
#COPY --from=builder /target/release/massa-client /source/massa-client
#
#COPY --from=builder /massa-node/config /source/massa-node/config
#COPY --from=builder /massa-node/base_config /source/massa-node/base_config
#COPY --from=builder /target/release/massa-node /source/massa-node

EXPOSE 31244 31245 33034 33035
