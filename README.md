Call Center Problem
==========================

Imagine you have a call center with three levels of respondents: respondent, manager, and director. An incoming telephone call must be  first allocated to a respondent who is free. If the respondent can't handle the call, he or she must escalate the call to a manager. If the manager is not free or not able to handle it, then the call should be escalated to a director. Design the classes and data structures for this problem. Implement a solution that assigns and dispatches a call to the first available respondent.

## Features

- Use any language of your choice.
- The solution has to be tested.
- The solution has to be documented.
- Write the solution as if you were gonna ship it to a production environment.


## Python & Required Libraries
Of course, you obviously need Python. Python 2 is already preinstalled on most systems nowadays, and sometimes even Python 3. You can check which version(s) you have by typing the following commands:

    $ python --version   # for Python 2
    $ python3 --version  # for Python 3

Any Python 3 version should be fine, preferably ≥3.5. If you don't have Python 3, I recommend installing it (Python ≥2.6 should work, but it is deprecated so Python 3 is preferable). To do so, you have several options: on Windows or MacOSX, you can just download it from [python.org](https://www.python.org/downloads/). On MacOSX, you can alternatively use [MacPorts](https://www.macports.org/) or [Homebrew](https://brew.sh/). On Linux, unless you know what you are doing, you should use your system's packaging system. For example, on Debian or Ubuntu, type:

    $ sudo apt-get update
    $ sudo apt-get install python3

Another option is to download and install [Anaconda](https://www.continuum.io/downloads). This is a package that includes both Python and many scientific libraries. You should prefer the Python 3 version.

If you choose to use Anaconda, read the next section, or else jump to the [Using pip](#using-pip) section.

## Using Anaconda
When using Anaconda, you can optionally create an isolated Python environment dedicated to this project. This is recommended as it makes it possible to have a different environment for each project (e.g. one for this project), with potentially different libraries and library versions:

    $ conda create -n callcenter python=3.5
    $ source activate callcenter

This creates a fresh Python 3.5 environment called `callcenter` (you can change the name if you want to), and it activates it. This environment contains all the libraries that come with Anaconda. 

## Using pip 
If you are not using Anaconda, you need to install Python libraries that are necessary for this project. For this, you can either use Python's integrated packaging system, pip, or you may prefer to use your system's own packaging system (if available, e.g. on Linux, or on MacOSX when using MacPorts or Homebrew). The advantage of using pip is that it is easy to create multiple isolated Python environments with different libraries and different library versions (e.g. one environment for each project). The advantage of using your system's packaging system is that there is less risk of having conflicts between your Python libraries and your system's other packages. Since I have many projects with different library requirements, I prefer to use pip with isolated environments.

These are the commands you need to type in a terminal if you want to use pip to install the required libraries. Note: in all the following commands, if you chose to use Python 2 rather than Python 3, you must replace `pip3` with `pip`, and `python3` with `python`.

First you need to make sure you have the latest version of pip installed:

    $ pip3 install --user --upgrade pip

The `--user` option will install the latest version of pip only for the current user. If you prefer to install it system wide (i.e. for all users), you must have administrator rights (e.g. use `sudo pip3` instead of `pip3` on Linux), and you should remove the `--user` option. The same is true of the command below that uses the `--user` option.

Next, you can optionally create an isolated environment. This is recommended as it makes it possible to have a different environment for each project (e.g. one for this project), with potentially very different libraries, and different versions:

    $ pip3 install --user --upgrade virtualenv
    $ virtualenv -p `which python3` env

This creates a new directory called `env` in the current directory, containing an isolated Python environment based on Python 3. If you installed multiple versions of Python 3 on your system, you can replace `` `which python3` `` with the path to the Python executable you prefer to use.

Now you must activate this environment. You will need to run this command every time you want to use this environment.

    $ source ./env/bin/activate

Next, use pip to install the required python packages. If you are not using virtualenv, you should add the `--user` option (alternatively you could install the libraries system-wide, but this will probably require administrator rights, e.g. using `sudo pip3` instead of `pip3` on Linux).

    $ pip3 install --upgrade -r requirements.txt

Great! You're all set.

## Running The Automated Tests

    $ py.test tests/

## CLI

Set environment

    $ export ENVIRONMENT='local'
    $ export ENVIRONMENT='production'

Run the sample server

    $ python main.py

Try the endpoints:

| Endpoint | Web Verb | Function |
| :---         |     :---:      |          ---: |
| /call-center/api/v1.0/add_respondent   | POST     | Adds a respondent to the queue. Expects {"respondent_type":"respondent"},  {"respondent_type":"manager"} or {"respondent_type":"director"} in body.    |
| /call-center/api/v1.0/make_call    | GET       | Makes a particular call so it can be dispatched to the available respondent.      |
| /call-center/api/v1.0/complete_call   | GET       | Completes call from a particular respondent.     |
| /call-center/api/v1.0/status   | GET       | Gets the status and rank of each of the respondents on the queue.     |

## Docker

There is no need to install 3rd-party apps on the system – you can run it in containers. Docker also gives you the ability to run different versions of same application simultaneously.

### Run Your Image

Now you are ready to build an image from this Dockerfile. Run:

    $ docker build -t python-call-center .

After your image has been built successfully, you can run it as a container. In your terminal, run the command docker images to view your images. You should see an entry for “python-call-center”. Run the new image by entering:

    $ docker run -d -p 5000:5000 python-call-center -e ENVIRONMENT='local'
