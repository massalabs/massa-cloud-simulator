# Base Image
FROM debian:bullseye 

# Install Git and NECESSARY DEPENDENCIES

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y python3 python3-venv pkg-config curl git build-essential libssl-dev libclang-dev -y expect cmake && \
    apt clean -y

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"


# Copy Rust project files to the container from git repo


RUN git clone  --depth=1 --branch flag_private_addresses https://github.com/massalabs/massa.git

WORKDIR /massa

COPY  /base_config/initial_ledger.json massa-node/base_config/initial_ledger.json
COPY  /base_config/initial_vesting.json massa-node/base_config/initial_vesting.json


RUN apt-get update && apt-get install -y expect
# RUN echo 1 | curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# RUN . $HOME/.cargo/env
RUN rustup toolchain install nightly-2023-02-27
RUN rustup default nightly-2023-02-27

# RUN export PATH="$PATH:$HOME/.cargo/bin"


RUN cargo build --features "sandbox local_network"

RUN chmod +x /massa/massa-node

WORKDIR /massa/massa-node/
CMD ["cargo", "run", "--features", "sandbox local_network", "--", "-p", "test"]

# docker run -it -p 33035:33035 -p 33036:33036  massa_node:v7

#------ cleaning
#delete all the directories staring with massa and C
# RUN find . -type d -name "massa*" -exec rm -r {} \; -prune !("massa-api") 
# RUN find  . -name 'C*' -exec rm {} \;
# RUN rm README.md bors.toml rust-toolchain.toml   

# RUN find . -type d -name 'massa*' -not -name 'massa-api' -not -name 'massa-api-exports' -exec rm -r {} \;

# RUN find . -maxdepth 1 -type d -name 'massa*' ! -name 'massa-api' ! -name 'massa-api-exports' -exec rm -rf {} +

## for run
# RUN cd massa-node
# RUN cargo run --bin massa-node

#docker run -it -d -p 33035:33035 -p 33036:33036 arshavee/massa-node:v11