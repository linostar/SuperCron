# SuperCron
Intelligent interface to cron in UNIX systems.

## Installation

Run `pip install supercron`.

## SuperCron vs classical crontab
SuperCron is based on crontab, while providing the following additional advantages:
- it can run interactively or non-interactively.
- it allows controlling several jobs simultaneously if they were assigned the same job name.
- it provides more options to handle jobs: adding, removing, searching, enabling, disabling, etc.
- it allows a vast and flexible amount of repetition sentences.
- it allows trigger-induced jobs based on the states of other jobs.
- it is more friendly especially to new sysadmins.

## Usage

SuperCron can run either in interactive mode or non-interactive mode.

**Interactive mode:**

Run `supercron` without any arguments to start interactive mode. You will prompted to choose an action, and then to enter action parameters (like `name`, `command` and `repetition`) if any.

**Non-interactive mode:**

In non-interactive mode, one of the following options can be used after the command name `supercron`.

- option `-h` or `--help`: shows the help message, with some usage examples
- option `-V` or `--version`: displays the version number

Additionally, one of the following subcommands can be used: add, delete, enable, disable, search, clear, trigger.

***Subcommand add***
- option `-h` or `--help`: shows the help message of the subcommand
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- option `-c` or `--command`: required; here goes the command to be executed
- option `-r` or `--repetition`: required; the repetition sentence (see examples below)
- argument `name`: required; represents the job name which will be added (several jobs can share the same name)

***Subcommand rename***
- option `-h` or `--help`: shows the help message of the subcommand
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- argument `old_name`: required; old name of the job(s) (several jobs can share the same name)
- argument `new_name`: required; new name of the job(s) (several jobs can share the same name)

***Subcommands delete, enable and disable***
- option `-h` or `--help`: shows the help message of the subcommand
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- argument `name`: required; represents the job name on which the action will occur (several jobs can share the same name)

***Subcommand search***
- option `-h` or `--help`: shows the help message of the subcommand
- argument `name`: required; the exact job name to search for, or `@supercron` to list all SuperCron jobs, or `@all` to list all user's crontab entries

***Subcommand clear***
- option `-h` or `--help`: shows the help message of the subcommand
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- option `-f` or `--force`: skips asking for confirmation before clearing all jobs

Note: this subcommand will only clear SuperCron jobs from user's crontab.

***Subcommand trigger***
- option `-h` or `--help`: shows the help message of the subcommand
- option `-q` or `--quiet`: optional; suppresses all output and error messages
- option `-t` or `--trigger`: trigger in the form of "none" or "*ACTION* if *NAME* is *STATE*". See **Triggers** section below.
- argument `name`: required; represents the triggered job name on which *ACTION* will occur (several jobs can share the same name)

## Triggers
Triggers can take one of 2 forms:
- "none" for removing the previous trigger
- "*ACTION* if *NAME* is *STATE*" for adding a new trigger or replacing an old one

*ACTION* is the action applied on the enabled state of the triggered job and it can be `on`, `off` or `toggle`.

*NAME* is the name of the triggering job.

*STATE* is the triggering state of the triggering job, and it can be `enabled`, `disabled`, `toggled`, `added` or `deleted`.

Using action `toggle` means to enable the triggered job if it was disabled, and to disable it if it was enabled.

State `toggled` activates the trigger when the triggering job is enabled or disabled.

Note that when a job is renamed from *name1* to *name2*, it means activating triggers that end with `if name1 is deleted` and triggers that end with `if name2 is added`, since a rename is considered a deletion of the old job name and an addition of the new job name.

## Examples
- Add a job:
```
supercron add -c "date +%j >> log_file" -r "every 2 days" log_dates
supercron add -c "scp -r /path1 user@server:/path2" -r "at 11:50 pm on mondays" backup_server
```
- Rename a job:
```
supercron rename log_dates log_all_dates
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
- Add a trigger:
```
supercon trigger -t "on if log_months is off" log_days
```
- Remove a trigger:
```
supercron trigger -t none log_days
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
- on 14 May
- in september
- in sep
- from may to august
- from dec to feb
- in january and april
- in jan, aug, oct

Repetition sentences can also be any (unsorted) logical mix of the above. For example:
- at 09:00 every 3 days
- from june to november every 2 hours
- every 30 minutes on fri and sat
- midnight from monday to friday in october and december
