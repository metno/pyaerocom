FROM mcr.microsoft.com/devcontainers/python:1-3.13

# System packages needed by cartopy/pyproj/cf-units based dependencies.
# -----------------------------------------------------------------------------
#  Fix yarn signature issue, open bug with microsoft images
#   https://github.com/devcontainers/images/issues/1752
# -----------------------------------------------------------------------------
RUN curl -fsSL https://dl.yarnpkg.com/debian/pubkey.gpg \
  | sudo gpg \
        --batch \
        --yes \
        --dearmor \
        -o /usr/share/keyrings/yarn-archive-keyring.gpg
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libudunits2-dev \
        libgeos-dev \
        libproj-dev \
        proj-data \
        proj-bin \
    && rm -rf /var/lib/apt/lists/* \
RUN mkdir /lustre/storeB

