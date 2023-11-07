set dotenv-load := true

@_default:
    just --list

##################
#  DEPENDENCIES  #
##################

bootstrap:
    python -m pip install --editable '.[dev]'

pup:
    python -m pip install --upgrade pip

update:
    @just pup
    @just bootstrap
