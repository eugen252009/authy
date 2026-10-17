#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-only
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec python3 "$ROOT/scripts/authy.py" build "$@"
