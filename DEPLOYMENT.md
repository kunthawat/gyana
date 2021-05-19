# https://beta.gyana.com

## Setup

Below describes the steps to create this deployment from scratch

### Google Cloud Platform

---

Created a separate project within the `gyana.co.uk` company called `Gyana Beta`

Important attributes within this project:

- [Google sheets API enabled](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com)
- All developer emails added in IAM with the following roles:
  - `Cloud KMS Admin`
  - `Cloud KMS CryptoKey Encrypter/Decrypter`
  - `Editor`
- A service account which:
  - Has its email is set to the `GCP_BQ_SVC_ACCOUNT` env variable
  - Has `BigQuery Admin` role in IAM
  - Has `Storage Object Creator` role in IAM
  - Has `Storage Object Viewer` role in IAM

#### **BigQuery**

In the BQ explorer add the following two datasets under the `gyana-beta` project:

- `heroku_integrations`
- `heroku_dataflows`

These two values are derived from `DATASET_ID` and `DATAFLOW_ID` in `lib/clients.py`. This is similar to the `just mk_bq` command that needs to be run on local development setup.

### Heroku

---

A [gyana-beta](https://dashboard.heroku.com/apps/gyana-beta) has been created using the following commands.

```zsh
# Using --remote here to add a remote to the local git config
heroku create --region=eu --remote beta --addons=heroku-postgresql,heroku-redis
```

After creation a first deployment was pushed

```zsh
git push beta main
```

Some helpful commands

```zsh
# When a heroku app gets created from the cli it gets assigned a random name
# After renaming the deployment running the following commands will fix the remote
git remote rm beta
heroku git:remote -a <Heroku_environment_name> -r beta
```

#### **Custom domain**

On the Heroku settings page a custom domain `beta.gyana.com` is added. To get the wildcard `*.gyana.com` SSL working the .key en .pem file from LastPass are uploaded into the Heroku system. This SSL combo will then be used for that domain. Heroku also generates a `DNS Target` that will be used for the GoDaddy step below.

#### **Env variables that matter**

These config variables are set in the [Settings](https://dashboard.heroku.com/apps/gyana-beta/settings) tab in the Heroku web app

- `DJANGO_SETTINGS_MODULE` = `gyana.settings.heroku`
- `GOOGLE_APPLICATION_CREDENTIALS` = `google-credentials.json`
- `GOOGLE_CREDENTIALS` = `<credential_json_from_svc_account>`
- `SECRET_KEY` = `<secret_key_val>`
- `GCP_PROJECT` = `gyana-beta`
- `GCP_BQ_SVC_ACCOUNT` = `gyana-beta@gyana-beta.iam.gserviceaccount.com`
- `EXTERNAL_URL` = `https://beta.gyana.com`
- `CLOUD_NAMESPACE` = `heroku`

### GoDaddy

---

To setup the DNS created in the Heroku settings we need to add a CNAME record with:

- `Host`: `beta`
- `Points to`: `<DNS_TARGET from Heroku settings>`
- `TLS`: `600s`
