# Item Catalog Project

## Project Overview

An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Usage

Usage Text

## Installation

### Source files and dependencies

First head to the directory you want to install the app then:

```bash
git clone https://github.com/Scheercuzy/FSND-catalog-project.git
cd FSND-catalog-project/
```

If you wish to run this app globally on your system, you can skip the installation of the virtual environment but its highly recommended not to do so. To install a virtual environment run:

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

Now installed the requirements for the project app with:

```bash
pip install -r requirements.txt
```

### Environment Variables

A few environment variables needs to be set to be able to run this App. The first 2 are to disable the https check as the app will be run on a development server instead of a production server with a load balancer installed. These environment variables will need to be set every time you open a new terminal window as the variables are forgotten when the window is closed. To disable the https check, run:

```bash
export OAUTHLIB_INSECURE_TRANSPORT=1
export OAUTHLIB_RELAX_TOKEN_SCOPE=1
```

You will also need to setup the client id and client secret for the oauth system in the app. The enviroment variables to set are

```bash
export GOOGLE_CLIENT_ID=<google_client_id_here>
export GOOGLE_CLIENT_SECRET=<google_client_secret_here>
```

### Running the App

Now the installation is done, but the first time you run the app you have to initialize the database with the argument of `--setup`

```bash
python run.py --setup
```

All the subsequent times, run it normal with `run.py`

```bash
python run.py
```