# AI-Joker
Joke generator based on a LSTM language model trained on the reddit jokes dataset. It contains both a jupyter notebook for training it, and code to create a docker container that runs it.

# Research
The research folder contains a Jupyter Notebook that shows the process of training the LSTM based language model. This jupyter results in the vocabulary and model file that can be used.

# Production
Contains both a Python wrapper for using the model alogside a Flask app and Dockerfile to get it to production. It is the Dockerfile that results in a docker container that can be deployed to the cloud.

It has been used to deploy a Docker container on Heroku to be used on my blog entry [here](https://victorbusque.github.io/AI-Joker-m%C3%A1quinas-bromean/).
