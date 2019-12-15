Tilty
=====

A python module and CLI to capture and emit events from your [tilt hydrometer](https://tilthydrometer.com/)

I've been unhappy with the quality/inconsistency of what I've seen out there in terms of random scripts that capture.
No tests, no pluggable emitters, hard to find, etc.

The tilt essentially broadcasts iBeacon packets to send out a uuid (which type of tilt it is), a major (the temp in F), and a minor (the specific gravity).

This will capture those whenever theyre transmitted and emit them to a backend of your choosing so that you can graph it over time asynchronously.

The Tilt supports writing to a google doc which you could use with something like IFTTT or Zapier, but this is much lighter and lets you decide how you want to push that out with a pluggable backend system.


## TODO ##

Right now all it does is log to STDOUT.
As it progresses it will have pluggablel emitters such as:

  * InfluxDb
  * Webhooks
  * SNS

  etc


## Usage ##

### As a cli ###

```
$ tilty
```

### From docker ###

```
$ docker-compose build
$ docker-compose run tilty
```

## Installation ##

```
$ git clone https://github.com/myoung34/tilty
$ pip install -e .
```
