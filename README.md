# Item Catalog Project

## Project Overview

An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Usage

The application starts out with a blank database, so once you've got the app up and running you will be directed to the index page were you will see a navbar with the title and the ability to login and 2 tabs. The 2 tabs will have the heading of categories and items. To start adding categories and items, you will first need to login, the only option for this app is to login with google. once logged in, you will have the option to add categories and items as you please. Once created, you will have the option to edit each entry or delete them also. You will not be able to delete a category if items are linked to it.

The application also has a couple json endpoints. They are:

- `/json/all`: Shows all the categories and the items associated with them
- `/json/categories`: Shows all the categories
- `/json/items`: Shows all the items
- `/json/category/<category_id>`: Shows the category with the category_id of `<category_id>`
- `/json/item/<item_id>`: Shows the item with the item_id of `<item_id>`

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

A few environment variables needs to be set to be able to run this App. The first 2 are to disable the https check as the app will be run on a development server instead of a production server with a load balancer installed. These variables will already be set for you in the .env file in the parent directory

You will also need to setup the client id and client secret for the oauth system in the app. The environment variables to set are `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`. Once obtained from Google, add them to the `.env` file in the parent directory

```bash
GOOGLE_CLIENT_ID=<client_id_here>
GOOGLE_CLIENT_SECRET=<client_secret_here>
```

Alternatively you can set them on the current terminal window by exporting them instead like this:

```bash
export GOOGLE_CLIENT_ID=<client_id_here>
export GOOGLE_CLIENT_SECRET=<client_secret_here>
```

The application will not run without these variables

### Running the App

Now the installation is done, but the first time you run the app you have to initialize the database with the argument of `--setup`

```bash
python run.py --setup
```

All the subsequent times, run it normal with `run.py`

```bash
python run.py
```
