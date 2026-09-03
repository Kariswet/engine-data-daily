APPNAME=get-data-daily
TAG=1.0.0

echo "DEPLOYING APPLICATION"

if [ $(docker ps -aq -f name=^${APPNAME}$) ]; then
    echo "Stopping and removing old container..."
    docker stop $APPNAME
    docker rm $APPNAME
fi

echo "Building new image..."
docker build -t $APPNAME .
docker tag $APPNAME $APPNAME:$TAG

echo "Starting new container..."
docker container run -d --env-file /home/wsltyq/analyze-market/.env-daily --name $APPNAME --restart always --log-opt max-size=50m -m 1g --cpus=\"1\" $APPNAME:$TAG

docker image prune -f

echo "DEPLOYMENT SUCCESS"
docker ps -f name=^${APPNAME}$