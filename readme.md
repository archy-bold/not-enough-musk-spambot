# Reddit Comment Bot
This Reddit Comment Bot is a python-based auto-responder.
  - Pick a subreddit to scan
  - Designate a specific comment to search for
  - Set your bot's reply

### Install

```bash
# Install dependencies
pip install -r requirements.txt
# Setup the sqlite db
python setup.py
```

### Requirements
  - [Python](https://www.python.org/downloads/)
  - [Praw](https://praw.readthedocs.io/en/latest/getting_started/installation.html)
  - A Reddit Account

### Setup
###### Reddit App:
1. [Navigate to the Apps page ](https://www.reddit.com/prefs/apps/)
2. Click *create an app*
3. **name:** Set a name for your app
4. **type:** Script
5. **description:** Optional
6. **about url:** Optional
7. **redirect uri:** http://localhost:8080
8. Note the outputted *client id* and *secret*

###### .env:
```bash
cp .env.example .env
```
1. **BOT_NAME:** your Reddit username
2. **PASSWORD:** your Reddit password
3. **CLIENT_ID:** the outputted client id
4. **CLIENT_SECRET:** the outputted secret

###### reddit_bot.py:

Set the subreddit to search (default = "r/test"):
```python
r.subreddit('test')
```
Comment search criteria (default = "sample user comment"):
```python
if "sample user comment"
```
Bot's comment reply (default = "Hey, I like your comment!"):
```python
comment.reply("Hey, I like your comment!")
```

### Usage

Navigate into the bot directory.
Run your bot:
```sh
$ python reddit_bot.py
```

#### Docker

It's possible to containerise the script.

To build it:

```sh
docker build -t reddit_bot -f .docker/reddit_bot/Dockerfile .
```

Then run with:

```sh
docker run -e SUBREDDIT=test -e SLEEP=0 -e SUBMISSION_PROBABILITY=0.25 -e COMMENT_PROBABILITY=0.1 -e REPLY_AGE=4 -e ENV=test -e MODE=once -e BOT_NAME=xxx -e PASSWORD=xxx -e CLIENT_ID=xxx -e CLIENT_SECRET=xxx reddit_bot
```

### Phrase Sources

For a rundown of the phrases and their sources, see [phrases.md](phrases.md). Yes, Elon Musk has said everything this dumb bot repeats.

### Credits

- [u/citycentre95 for convincing me to do this and a few ideas](https://www.reddit.com/r/EnoughMuskSpam/comments/10fivfd/comment/j4zebju/?utm_source=reddit&utm_medium=web2x&context=3).
- [u/Which_way_witcher](https://www.reddit.com/r/EnoughMuskSpam/comments/10muplo/a_leaked_internal_message_appears_to_show_elon/j66cjrf/?context=3) for a few more ideas.
- [u/RespondNo4954](https://www.reddit.com/r/EnoughMuskSpam/comments/10tl1ef/petition_to_unban_unotenoughmuskspam/?utm_source=share&utm_medium=ios_app&utm_name=iossmf) for starting a petition to unban the bot, and succeeding!
- [u/throwaway3292923](https://www.reddit.com/u/NotEnoughMuskSpam/comments/113s6wc/comment/jbcmtqz/?utm_source=share&utm_medium=web2x&context=3) for joining the discussion with a suggestion, "It's a hit piece".
- [u/Hot-Bint](https://www.reddit.com/user/Hot-Bint/) for a bunch of ideas.
- Everyone on [r/EnoughMuskSpam](https://www.reddit.com/r/EnoughMuskSpam/) who had something nice to say about the bot. Very few of the things I make gets feedback like this.
