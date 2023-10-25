FROM postgres:14-alpine

RUN apk add --no-cache curl bash sudo

RUN curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | sudo bash

ENV NEW_RELIC_API_KEY=NRAK-NMQ4H8KEQIMNU3EPQFT4MAP5UT9
ENV NEW_RELIC_ACCOUNT_ID=4152035
ENV NEW_RELIC_REGION=EU

RUN sudo /usr/local/bin/newrelic install -n postgres-open-source-integration
