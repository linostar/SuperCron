# SuperCron
[![Build Status](https://travis-ci.org/linostar/SuperCron.svg?branch=master)](https://travis-ci.org/linostar/SuperCron)

Intelligent interface to cron in UNIX systems.

## Installation

Run `pip install supercron` or `easy_install supercron`.

## Usage

SuperCron can run either in interactive mode or non-interactive mode.

**Interactive mode:**

Run `supercron` without any arguments to start interactive mode. You will prompted to choose an action, and then to enter action parameters (like `name`, `command` and `repetition`) if any.

**Non-interactive mode:**

In non-interactive mode, at least one of the following options/arguments has to be used after the command name `supercron`.

- option `-h` or `--help`: shows the help message, with some usage examples
- option `-V` or `--version`: displays the version number

Additionally, one of the following subcommands can be used: add, delete, enable, disable, search, clear.

***Subcommand add***
- option `-h` or `--help`: shows the help message of the subcommand
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- option `-c` or `--command`: required; here goes the command to be executed
- option `-r` or `--repetition`: required; the repetition sentence (see examples below)
- argument `name`: required; represents the job name which will be added

***Subcommands delete, enable and disable***
- option `-h` or `--help`: shows the help message of the subcommand
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- argument `name`: required; represents the job name on which the action will occur

***Subcommand search***
- option `-h` or `--help`: shows the help message of the subcommand
- argument `name`: required; the exact job name to search for, or `@supercron` to list all SuperCron jobs, or `@all` to list all user's crontab entries

***Subcommand clear***

It will only clear SuperCron jobs from user's crontab:
- option `-h` or `--help`: shows the help message of the subcommand

## Examples
- Add a job:
```
supercron add -c "date +%j >> log_file" -r "every 2 days" log_dates
supercron add -c "scp -r /path1 user@server:/path2" -r "at 11:50 pm on mondays" backup_server
```
- Delete a job:
```
supercron delete log_dates
```
- Enable a job:
```
supercron enable log_dates
```
- Disable a job:
```
supercron disable log_dates
```
- Search jobs:
```
supercron search log_dates
supercron search @supercron
supercron search @all
```
- Clear all SuperCron jobs:
```
supercron clear
```

## Repetition sentences
Repetition sentences are provided in a `supercron add` command directly after the `-r` or `--repetition` option.

Examples of accepted repetition sentences (case insensitive):
- everyday
- at midnight
- every 5 minutes
- once every 2 hours
- every 10 days
- every 4 months
- on mondays
- on monday, wednesday and friday
- from saturday to tuesday
- on fri
- on mon, wed and fri
- from mon to thu
- at 11:50
- at 23:50
- at 10:10 am
- at 10:10 pm
- on 19/5
- in september
- in sep
- from may to august
- from dec to feb
- in january and april
- in jan, aug, oct

Repetition sentences can also be any logical mix of the above. For example:
- at 09:00 every 3 days
- from june to november every 2 hours
- every 30 minutes on fri and sat
- midnight every 2 days from monday to friday in october and december
