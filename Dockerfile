############# BUILDTIME #############
# BuildTime Image
FROM rustlang/rust:nightly AS BuildTime

# Define env variables
ARG BUILD_USER
ARG USER_PSWD

# Update the machine
RUN apt-get update -y

# Upgrade the machine
RUN apt-get upgrade -y

# Install required packages
RUN apt-get install pkg-config \
                    git \
                    build-essential \
                    clang \
                    libclang-dev -y

# Configure the path for rust
ENV PATH="/root/.cargo/bin:${PATH}"

# Install nigthly using rustup
RUN rustup toolchain install nightly-2022-11-14

# Set nigthly as default
RUN rustup default nightly-2022-11-14

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Create the user $USER
RUN useradd $BUILD_USER -m -u 1001

# Set the username $USER and the password $USER_PSWD
RUN echo "$BUILD_USER:$USER_PSWD" | chpasswd

# Clone the repository
RUN git clone --branch testnet https://github.com/massalabs/massa.git

# Move to the directory massa
WORKDIR /massa

# Build massa-node and the massa-client
RUN cargo build --release --bin massa-node --bin massa-client 


############# RUNTIME #############
# Production Image
FROM debian:bullseye-slim AS runtime

# Define env variables
ARG BUILD_USER
ARG USER_PSWD
ARG NODE_PSWD

# Update the machine
RUN apt-get update -y

# Upgrade the machine
RUN apt-get upgrade -y

# Clears out the local repository of retrieved package files
RUN apt-get clean -y

# Create the user $USER
RUN useradd $BUILD_USER -m -u 1001

# Set the username $USER and the password $USER
RUN echo "$BUILD_USER:$USER_PSWD" | chpasswd

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

# Change the permission of the folder
RUN chown -R $BUILD_USER:$BUILD_USER /home/$BUILD_USER/*

# Expose ports used by Massa
#EXPOSE 33034 33035 31244 31245

# Move to the directory massa_exec_files
WORKDIR /home/$BUILD_USER/massa_exec_files/massa-node/
