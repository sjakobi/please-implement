# [please implement](http://please-implement.appspot.com/)

A website with an overview of unimplemented exercises for [exercism.io](http://exercism.io)

Built on Google App Engine with the awesome [agithub](http://github.com/jpaugh/agithub) module.

## How to run this

Two files are missing in this repo:

* `please-implement/agithub.py`: Get it [here](http://github.com/jpaugh/agithub).
* `please-implement/config.py` which should look like this:

  ```Python
  username = 'valid-github-username'
  password = 'password'
  ```
  
Add these files and start a local development version with `dev_appserver.py please-implement`.

If this doesn't work please open an [issue](http://github.com/sjakobi/please-implement/issues)!
