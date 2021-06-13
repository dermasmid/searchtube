# Overview
You can use this project to make any youtube channel searchable.
Follow the instuctions bellow, and if you bump in to any issue, please open an issue.

You can see the site live [here](https://searchtube.site)

I know that UI is not pretty, I"m not soo good at those stuff, so if you are - please consider contibuting, thanks.

# Installation

```bash
git clone https://github.com/dermasmid/searchtube.git && cd searchtube
./setup.sh
cp .example.env .env
nano .env
make build
```

To add ssl run inside the container (make shell):
`certbot --apache -d yourdomain.com`

# Adding a channel

```bash
make shell
add_channel UCXv-co3EYHF7aOH4A93qAHQ "Lew later"
```

Replace the first argument with the channel id, and the second with the name of the channel - how you want it to be displayed on the site.

