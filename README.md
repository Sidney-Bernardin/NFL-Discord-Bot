# NFL-Discord-Bot

**Contents**
1. [Overview](#overview)
1. [Usage](#usage)

## Overview
This is a discord bot that lets users lookup the current stats of active NFL players by web-scraping nfl.com.

For more on how this project works, visit my [portfolio](https://sidney-bernardin.github.io/project/?id=nfl_discord_bot).

## Usage

### Running Locally
Running PubSub locally on your machine is as simple as cloning this repository.

``` bash
git clone https://github.com/Sidney-Bernardin/NFL-Discord-Bot.git
cd NFL-Discord-Bot
```

Setting the following environment variables.

``` bash
export TOKEN=your_token_here
export PREFIX=/
```

Then running the Python program yourself.

``` bash
python main.py
```

Or, run in a container using the Dockerfile at the root of this repository.

``` bash
docker build -t nfl_discord_bot .
sudo docker run -it -e PREFIX=/ -e TOKEN=your_token_here sidneybernardin/nfl_discord_bot
```

### Commands

#### Stat
Lets users select stats of a game/year from an active NFL player's career.
<div align=left>
  <img src="./pictures/pic1.png" width="50%" />
</div>

#### Help
Gives users instructions for use the bot.
<div align=left>
  <img src="./pictures/pic2.png" width="50%" />
</div>
