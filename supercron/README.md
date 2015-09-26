# SuperCron

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
- option `-h` or `--help`: shows the help message
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- option `-c` or `--command`: required; here goes the command to be executed
- option `-r` or `--repetition`: required; the repetition sentence (see examples below)
- argument `name`: required; represents the job name which will be added

***Subcommands delete, enable and disable***
- option `-h` or `--help`: shows the help message
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- argument `name`: required; represents the job name on which the action will occur

***Subcommand search***
- option `-h` or `--help`: shows the help message
- argument `name`: required; the exact job name to search for, or `@supercron` to list all SuperCron jobs, or `@all` to list all user's crontab entries

***Subcommand clear***
It will clear only SuperCron jobs from user's crontab:
- option `-h` or `--help`: shows the help message
