# Python bot for discord

This is a custom discord bot built mainly for the `No !Auh` variety gaming discord server.

This bot is dockerized, and will easily run on a t2.nano which allows for a cheap run cost. 

This bot also holds state with various features via a json file that is stored in an s3 bucket, which will need to be provided via a .env file.

### Features

Current features include the following:

```
GamerInfo:
  battlenet         Update gamer info with Battle.net username
  epic              Update gamer info with Epic username
  gamer.info        Lists the gamer-info for a Discord member
  origin            Update gamer info with Origin username
  psn               Update gamer info with PSN username
  rockstar          Update gamer info with RockStar username
  steam             Update gamer info with Steam username
  switch            Update gamer info with Switch username
  switch.friendcode Update gamer info with Switch friend code
  twitch            Update gamer info with Twitch username
  xbox              Update gamer info with Xbox username
Groups:
  group.create      Creates a notification group
  group.delete      Deletes a notification group
  group.list        List all notification groups
  member.add        Adds a member to a notification group
  member.list       Lists all members in a notification group
  member.remove     Removes a member from a notification group
  notify            Sends a message to all members of a notification group - ...
Utility:
  give.koroks         Give a member a Korok seed! (Karma points)
  list.koroks         Find out how many Korok seeds a member has
  roll.dice         Rolls X dice with Y sides
No Category:
  help              Shows this message

Type !help command for more info on a command.
You can also type !help category for more info on a category.
```

### GamerInfo

This allows users to set usernames or gamer tags for the supported game clients or consoles. Users can then use `!gamer.info @userMention` to retrieve the settings a member has stored. 

### Groups

Functionality to support creating groups, and adding members to groups in order to mass notify select members. 

### Koroks

Karma system in order to give users "Korok seeds" as a reward. Users can look up how many Korok seeds he / she has obtained. 

## Installation

Copy the docker-compose file and run on a server using `docker-compose.yaml`

`docker-compose up -d --build`

.env file must be in same directory as docker-compose.yaml and have the following variables defined:

```
DISCORD_TOKEN=<Your discord bot token>
DISCORD_GUILD=<Name of your discord server / guild>
DISCORD_S3_BUCKET=<bucket name in s3>
AWS_ACCESS_KEY_ID=<AWS user access key id>
AWS_SECRET_ACCESS_KEY=<AWS user secret access key>
AWS_DEFAULT_REGION=<default aws region>
```

## State

The discord bot keeps state through a json file stored in s3. If no state file exists, one will be created called `<DISCORD_GUILD>-state.json`. You should backup this state file
as it acts as the database for the discord bot. The bot will only pull down the s3 file on startup, and upload the file only when a change in state occurs. The bot keeps a local copy
of the file on disk to avoid having to read from s3 anytime a query happens, this keeps costs very low for the backend. 
