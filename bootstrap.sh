sudo apt install git-all
sudo apt-get update && sudo apt-get upgrade -y

sudo apt install docker.io -y
sudo systemctl start docker -y
sudo systemctl enable docker -y

curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

sudo groupadd docker
sudo gpasswd -a ubuntu docker

git clone --single-branch --branch Jean-Fraga https://github.com/JeanFraga/Blockchain.git
cd Blockchain

sudo docker-compose up --build