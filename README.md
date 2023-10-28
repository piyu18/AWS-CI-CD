# AWS-CI-CD

# Docker setup in EC2
sudo apt-get update -y

sudo apt-get upgrade

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

# Configure EC2 as self-hosted runner-
## Settings/Runners-Create self hosted runner and run the commands in EC2

# Github secrets
AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = us-east-1

AWS_ECR_LOGIN_URI = 224113744246.dkr.ecr.us-east-1.amazonaws.com

ECR_REPOSITORY_NAME = testapp