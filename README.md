# 4 4 TrueCry Miner (Linux Edition)
[![build-image](https://github.com/FM1337/44truecry-miner-docker/actions/workflows/build-image.yml/badge.svg)](https://github.com/FM1337/44truecry-miner-docker/actions/workflows/build-image.yml)

This is a working linux version of [TheZZAZZGlitch](https://www.youtube.com/c/TheZZAZZGlitch)'s 4 4 TrueCry

His script was introduced in [this video](https://youtu.be/rXZPhnVzc4M?t=474) but was pointed out that it was Windows only.

So, through a late-night to morning coding session, I got his script functioning on Linux, and in a docker container so that it (in theory) can be run pretty much any machine that supports Docker.

The original code was obtained from [here](https://sites.google.com/site/thezzazzglitch)

## Requirements
- **(Required)** Pokemon Yellow GBC Rom (US Release)
- **(Optional)** [Pushover](https://pushover.net/) User Key and Application Token for notifications when a result has been found
- **(Optional)** [Discord](https://discord.com/) Web Hook URL for notifications when a result has been found

## Usage
Assuming you've got everything installed for docker (I'm not walking you through installing Docker, you can use google for that), simply using the provided `docker-compose.yml` should get you up and running.

There's a provided `.env.example` file to show you the optional environment variables for notifications, to get them working, just create a file called `.env` in the same directory as where your docker-compose file is, and fill in the data if desired.

The Pokemon Yellow ROM (which by default unless you modify the host bindings) should be called `yellow.gbc` and present in the same directory as where the docker-compose file is.

You can either build the file locally, or use the provided dockerhub image (`fmcore/44truecryminer`) I created. If you don't know what you're doing, I recommend sticking with the pre-built one.

### Note
Due to how docker handles it logs, the live output will not work correctly if run with `docker-compose up`, you can kinda get around that by doing `docker-compose up -d` and then attaching to the container with `docker attach <container_id> --sig-proxy=false` which will allow you to `CTRL + C` out of the attachment withotu killing the container.

---
Assuming you've gotten everything in place correctly, all you need to do is the start the container and you're off to the race. If you got notifications set up, you should be good to just leave it running unintended (You can check in on it as you want to, but judging on the videos ZZAZZ posted about his script, it seems it's meant to be running for months, years or even decades before it'll get a result.)