# CONTRIBUTING


### GETTING STARTED
I recommend setting up a virtual enviroment since some of the packages are not compatible with python 3.13.1
```shell
virtualenv -p python3.12.0 .venv
source .venv/bin/activate 
pip install -r requirements.txt
```
If I am missing a requirement please let me know. 

### Continous Development
Installing the package in development mode:
```shell
pip install -e .
```

### Make a local .env file.
Make a local .env file, create an accounts in corresponding services and define the API keys in the .env file.
```shell
cp .env.example .env
```

### Building Frontend Locally. 

To set up the chat locally:
```shell

cd scholiumapp 
npm run dev

```

# Local Development
To start Scholium locally:
```shell
cd scholiumapp
# Starts Backend
npm run fastapi-run
# Starts Frontend
npm run dev
```


### 1. Fork & clone
- Click on the Fork button on GitHub
- Clone your fork
- Add the upstream repository as a new remote

### 2. Create a pull request

```shell
git checkout -b my_feature_branch
git commit -s
git push my_feature_branch

```

### 3. Update your pull request with latest changes

```shell
git checkout main
git pull upstream main
git checkout my_feature_branch
git rebase main
git push -f my_feature_branch
```

