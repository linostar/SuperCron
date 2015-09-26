# SuperCron

Intelligent interface to cron in UNIX systems.

## Installation

Run `pip install supercron` or `easy_install supercron`.

## Usage

SuperCron can run either in interactive mode or non-interactive mode.

**Interactive mode:**

Run `supercron` without any arguments to start interactive mode. You will prompted to choose an action, and then to enter action parameters (like `name`, `command` and `repetition`) if any.

**Non-interactive mode:**

In non-interactive mode, at least one of the following options/arguments has to be used after the command name `sueprcron`:

- option `-h` or `--help`: shows the full help message, with some usage examples
- option `-V` or `--version`: displays the version number
- option `-q` or `--quiet`: suppresses all output and error messages
- argument `name`: required unless `--help`/`-h` or `--version`/`-V` options are used; it represents the job name on which the action will occur
