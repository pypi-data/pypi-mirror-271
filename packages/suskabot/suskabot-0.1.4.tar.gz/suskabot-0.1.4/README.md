# Suskabot
Telegram Bot that really can do it all!

## Current functionality
1) Youtube video downloader. Send a link, get a video!
2) Translator. Fast translations without the need to specify to and from languages! Configure "default language to translate to" and "mother tongue". Currently supported languages: Russian, English, Ukranian
3) TBD: PDF manipulations

## Tests
To run the tests use:
```shell
poetry run pytest -v -s
```

## Usage

### Manual 
1) Create and activate a new virtual environment
``` shell
poetry shell
```
2) Install the project requirements
``` shell
poetry install
```
3) Set the API_TOKEN environment variable using export:
``` shell
export TG_BOT_API_TOKEN=<your TG bot api token>
```
or .env.secret:
``` shell
cd suskabot/config && echo TG_BOT_API_TOKEN=<your TG bot api token >> .env.secret
```
You can also start the app and .env.secret will be created for you with the key in place. 
Other environment variables can be conveniently set from .env.public
4) Start the app:
```shell
poetry run python suskabot/main.py
```

### Docker 
Specify this gitlab repositories container registry or build the image yourself:
 ``` shell
 docker build -t suskabot .
 docker run -d --env=TG_BOT_API_TOKEN=<TG bot api token> suskabot
 ```
