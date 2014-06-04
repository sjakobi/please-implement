# [please implement](http://please-implement.appspot.com/)

A website with an overview of unimplemented exercises for [exercism.io](http://exercism.io)

Built on Google App Engine with the awesome [agithub](http://github.com/jpaugh/agithub) module.

## How to run this

Three files are missing in the `please-implement` folder:

* `agithub.py`: Get it [here](http://github.com/jpaugh/agithub).
* `jinja2htmlcompress.py`: Get it [here](https://github.com/mitsuhiko/jinja2-htmlcompress).
* `config.py` which should look like this:

  ```Python
  username = 'valid-github-username'
  password = 'password'
  ```
  
Add these files and start a local development version with `dev_appserver.py please-implement`.

If this doesn't work please open an [issue](http://github.com/sjakobi/please-implement/issues)!
