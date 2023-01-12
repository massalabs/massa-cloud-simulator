############# BUILDTIME #############
# BuildTime Image
FROM rustlang/rust:nightly AS BuildTime

# Update the machine
RUN apt-get update -y

# Upgrade the machine
RUN apt-get upgrade -y

# Install required packages
RUN apt-get install pkg-config git build-essential clang libclang-dev -y

# Configure the path for rust
ENV PATH="/root/.cargo/bin:${PATH}"

# Install nigthly using rustup
RUN rustup toolchain install nightly-2022-11-14

# Set nigthly as default
RUN rustup default nightly-2022-11-14

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Clone the repository massa
RUN git clone --branch testnet https://github.com/massalabs/massa.git

# Move to massa directory
WORKDIR /massa

# Build massa-node and the massa-client
RUN cargo build --release --bin massa-node --bin massa-client --features sandbox


############# RUNTIME #############
# Production Image
FROM debian:bullseye-slim AS runtime

# Define env variables
ARG BUILD_USER
ARG USER_PWD
ARG NODE_PRIVKEY_FILE
ARG NODE_CONFIG_INITIAL_LEDGER
ARG NODE_CONFIG_INITIAL_ROLLS
ARG BOOTSTRAP_IP
ARG BOOTSTRAP_PUBK

# Update the machine
RUN apt-get update -y

# Upgrade the machine
RUN apt-get upgrade -y

# Install required packages
RUN apt-get install python3-venv \
                    procps nano curl -y
                    # procps, nano and curl are used for debugging inside the container

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Create the user $USER
RUN useradd $BUILD_USER -m -u 1001

# Set the username $USER and the password $USER
RUN echo "$BUILD_USER:$USER_PWD" | chpasswd

# Move to the directory massa_exec_files
WORKDIR /home/$BUILD_USER/massa_exec_files

# Copy the config and the binarie of Massa Client
COPY --from=BuildTime /massa/massa-client/config/  /home/$BUILD_USER/massa_exec_files/massa-client/config/
COPY --from=BuildTime /massa/massa-client/base_config/ /home/$BUILD_USER/massa_exec_files/massa-client/base_config/
COPY --from=BuildTime /massa/target/release/massa-client /home/$BUILD_USER/massa_exec_files/massa-client

# Copy the config and the binarie of Massa Node
COPY --from=BuildTime /massa/massa-node/config/ /home/$BUILD_USER/massa_exec_files/massa-node/config/
COPY --from=BuildTime /massa/massa-node/base_config/ /home/$BUILD_USER/massa_exec_files/massa-node/base_config/
COPY --from=BuildTime /massa/target/release/massa-node /home/$BUILD_USER/massa_exec_files/massa-node
COPY --from=BuildTime /massa/massa-node/base_config/config.toml /home/$BUILD_USER/massa_exec_files/massa-node/base_config/config.toml

# Change the permission of the folder
RUN chown -R $BUILD_USER:$BUILD_USER /home/$BUILD_USER/*

# Move to the directory massa_exec_files
WORKDIR /home/$BUILD_USER/massa_exec_files/massa-node/

# Copy local files to container
COPY requirements.txt .
COPY config.py .

# Create virtual env using python
RUN python3 -m venv venv

# Install requirements using pip
RUN venv/bin/pip install -r requirements.txt

# Update config.tolm file
RUN venv/bin/python config.py -e -c /home/$BUILD_USER/massa_exec_files/massa-node/base_config/config.toml -i "$BOOTSTRAP_IP" -a "$BOOTSTRAP_PUBK"


COPY $NODE_PRIVKEY_FILE /home/$BUILD_USER/massa_exec_files/massa-node/config/node_privkey.key
COPY $NODE_CONFIG_INITIAL_LEDGER /home/$BUILD_USER/massa_exec_files/massa-node/base_config/initial_ledger.json
COPY $NODE_CONFIG_INITIAL_ROLLS /home/$BUILD_USER/massa_exec_files/massa-node/base_config/initial_rolls.json
COPY wait_ts.sh /home/$BUILD_USER/massa_exec_files/massa-node
RUN rm -v /home/$BUILD_USER/massa_exec_files/massa-node/base_config/initial_peers.json
RUN echo "[]" >> /home/$BUILD_USER/massa_exec_files/massa-node/base_config/initial_peers.json

#COPY test_1.py /home/$BUILD_USER/massa_exec_files/massa-node
#COPY env_test.sh /home/$BUILD_USER/massa_exec_files/massa-node
