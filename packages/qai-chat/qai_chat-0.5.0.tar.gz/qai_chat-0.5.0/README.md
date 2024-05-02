# TODO

- Don't allow queries less than x characters long

# Installation

## Requirements

- [aws cli](https://aws.amazon.com/cli/) (Amazon Command Line Interface)
- [jq](https://jqlang.github.io/jq/) (json processor)
- [ecs-deploy](https://github.com/silinternational/ecs-deploy) (easy aws cli deployment script).

## Installing from private GitHub repo

git config --global url."https://${GITHUB_TOKEN}@github.com/Organization/repo-name".insteadOf "https://github.com/Organization/repo-name"

### Mac install

```sh
brew install aws-cli
```

```sh
brew install jq
```

```sh
curl https://raw.githubusercontent.com/silinternational/ecs-deploy/master/ecs-deploy | sudo tee /usr/bin/ecs-deploy
sudo chmod +x /usr/bin/ecs-deploy
```

##

## Qualified.com chatbot is good
