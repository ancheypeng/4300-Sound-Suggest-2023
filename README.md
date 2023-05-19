# SOUND SUGGEST

## Contents

- [SOUND SUGGEST](#sound-suggest)
  - [Contents](#contents)
  - [Summary](#summary)
  - [Running locally](#running-locally)
    - [Step 1: Set up a virtual environment](#step-1-set-up-a-virtual-environment)
    - [Step 2: Install dependencies](#step-2-install-dependencies)
    - [Step 3: Run server](#step-3-run-server)
  - [Maintaining the app](#maintaining-the-app)
    - [Spotify API Keys](#spotify-api-keys)

## Summary

This is the repository for the Sound Suggest App created for **"CS/INFO 4300 class at Cornell University"** during Spring 2023.

## Running locally

### Step 1: Set up a virtual environment
Create a virtual environment in Python. You may continue using the one you setup for assignment if necessary. To review how to set up a virtual environment and activate it, refer to A0 assignment writeup.

### Step 2: Install dependencies
You need to install dependencies by running `python -m pip install -r requirements.txt` in the backend folder.

### Step 3: Run server

Run the command `flask run` to start the local server.

## Maintaining the app

### Spotify API Keys
To maintain the app, the Spotify API keys may have to be changed. Currently, they are using a team member's spotify developer account, but the keys may expire/become invalidated in the future. The keys are located in the [spotify_ui.py](backend/helpers/spotify_ui.py) file. The variables `sound_suggest_id` and `sound_suggest_secret` will have to be changed.