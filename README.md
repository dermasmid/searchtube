# Installation

```bash
git clone && cd rextube
./setup.sh
cp .example.env .env
nano .env
make build
```

# Adding a channel

```bash
make shell
add_channel UCXv-co3EYHF7aOH4A93qAHQ "Lew later"
```

Replace the first argument with the channel id, and the second with the name of the channel - how you want it to be displayed on the site.

