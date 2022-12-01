# BuildTime Image
FROM debian:bullseye-slim AS BuildTime

ENV USER="user"

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
RUN rustup toolchain install nightly-2022-11-14

# Set nigthly as default
RUN rustup default nightly-2022-11-14

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Create the user ${USER}
RUN useradd ${USER} -m -u 1001

# Set the username ${USER} and the password ${USER}
RUN echo "${USER}:${USER}" | chpasswd

# Clone the repository
RUN git clone --branch testnet https://github.com/massalabs/massa.git

# Move to the directory massa
WORKDIR /massa

# Build massa-node and the massa-client
RUN cargo build --release --bin massa-node --bin massa-client 

############# RUNTIME #############
# Production Image
FROM debian:bullseye-slim AS runtime

ENV USER="user"
ARG PSWD_NODE="user"

# Update the machine
RUN apt-get update -y

# Install required packages
RUN apt-get install git \
                    python3 -y

# Upgrade the machine
RUN apt-get upgrade -y

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Create the user ${USER}
RUN useradd ${USER} -m -u 1001

# Set the username ${USER} and the password ${USER}
RUN echo "${USER}:${USER}" | chpasswd

# Clone the repository
RUN git clone --branch testnet https://github.com/massalabs/massa.git

# Move to the directory massa
WORKDIR /massa_exec_files

# Copy the config and the binarie of Massa Client
COPY --from=BuildTime /massa/massa-client/config/ /massa_exec_files/massa-client/config/
COPY --from=BuildTime /massa/massa-client/base_config/ /massa_exec_files/massa-client/base_config/
COPY --from=BuildTime /massa/target/release/massa-client /massa_exec_files/massa-client

# Copy the config and the binarie of Massa Node
COPY --from=BuildTime /massa/massa-node/config/ /massa_exec_files/massa-node/config/
COPY --from=BuildTime /massa/massa-node/base_config/ /massa_exec_files/massa-node/base_config/
COPY --from=BuildTime /massa/target/release/massa-node /massa_exec_files/massa-node

RUN chown -R ${USER}:${USER} /massa_exec_files/*

# Expose ports used by Massa
EXPOSE 31244 31245 33034 33035

# Move to the directory massa
WORKDIR /massa_exec_files/massa-node

# Run the node
#CMD ["/bin/sh", "./massa_exec_files/massa-node/massa-node -p ${PSWD_NODE} |& tee logs.txt"]

CMD ./massa-node -p ${PSWD_NODE} |& tee logs.txt

#ENTRYPOINT ["/bin/sh" "-c" "./massa_exec_files/massa-node/massa-node -p ${PSWD_NODE} |& tee logs.txt"]
