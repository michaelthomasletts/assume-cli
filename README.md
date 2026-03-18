<p align="center">
  <img 
    src="https://raw.githubusercontent.com/michaelthomasletts/assume-cli/refs/heads/main/docs/_static/transparent_header.png" 
    alt="assume" 
  />
</p>

<p align="center">
  <img 
    src="https://raw.githubusercontent.com/michaelthomasletts/assume-cli/refs/heads/main/docs/_static/transparent_header_assume.png" 
    alt="assume" 
  />
</p>

## Description

assume is a CLI tool with a daemon for exposing automatically refreshed temporary AWS credentials via [boto3-refresh-session](https://github.com/61418/boto3-refresh-session) to shells, SDKs, tools, and more. assume uses a UNIX domain socket with an in-memory session cache and a simple refresh loop.

## Commands

```
------
assume
------

Usage:
    assume [OPTIONS] <command> [ARGS]

Commands:
    assume      Configure the daemon and configs.
    config      Manage configs.
    export      Exports the specified config's credentials. 
    exec        Execute a one-off AWS command. 
    shell       Spawn an interactive shell to run AWS commands.
```

## Subcommands

```
-------------
assume daemon
-------------

Usage:
    assume daemon <subcommand> [OPTIONS]

Subcommands:
    start       Starts the daemon. 
    stop        Stops the daemon.
    logs        View daemon logs.

-------------
assume config
-------------

Usage:
    assume config <subcommand> [OPTIONS]

Subcommands:
    add         Creates a new config in the local config store.                                              
    list        Lists all stored configs names.                                                             
    get         Gets details of the specified config.                                                      
    update      Updates details of the specified config.                                                   
    remove      Removes the specified config. 
```