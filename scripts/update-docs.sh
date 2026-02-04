#!/bin/bash

# exit when any command fails
set -e

if [ -z "$1" ]; then
  ARG=-r
else
  ARG=$1
fi

if [ "$ARG" != "--check" ]; then
  tail -1000 ~/.opta/analytics.jsonl > opta/website/assets/sample-analytics.jsonl
  cog -r opta/website/docs/faq.md
fi

# README.md before index.md, because index.md uses cog to include README.md
cog $ARG \
    README.md \
    opta/website/index.html \
    opta/website/HISTORY.md \
    opta/website/docs/usage/commands.md \
    opta/website/docs/languages.md \
    opta/website/docs/config/dotenv.md \
    opta/website/docs/config/options.md \
    opta/website/docs/config/opta_conf.md \
    opta/website/docs/config/adv-model-settings.md \
    opta/website/docs/config/model-aliases.md \
    opta/website/docs/leaderboards/index.md \
    opta/website/docs/leaderboards/edit.md \
    opta/website/docs/leaderboards/refactor.md \
    opta/website/docs/llms/other.md \
    opta/website/docs/more/infinite-output.md \
    opta/website/docs/legal/privacy.md
