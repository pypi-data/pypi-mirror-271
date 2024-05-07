[macos]
platform_deps:
    brew install cmake automake autoconf

[linux]
platform_deps:
    echo "No platform_deps known"

deps: platform_deps
    cargo install cross
    poetry install

build-x86-linux-musl:
    RUSTFLAGS="-C target-feature=-crt-static" cross build --target x86_64-unknown-linux-musl --release

build-arm64-linux-musl:
    RUSTFLAGS="-C target-feature=-crt-static" cross build --target aarch64-unknown-linux-musl --release

build:
    cargo build --release

build-all: build-x86-linux-musl build-arm64-linux-musl build
