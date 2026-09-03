# APPNAME=catalog-creator
# TAG=1.0.0
# SERVER=192.168.107.22/imav2

# # GO111MODULE=on CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o $APPNAME .

# docker build -t $APPNAME .

# docker tag $APPNAME $SERVER/$APPNAME:$TAG
# echo "docker container run -d --env-file /home/ws/catalog-creator/.env1 --name $APPNAME-1 --restart always --log-opt max-size=50m -m 1g --cpus=\"1\" $SERVER/$APPNAME:$TAG"
# echo "docker container run -d --env-file /home/ws/catalog-creator/.env2 --name $APPNAME-2 --restart always --log-opt max-size=50m -m 1g --cpus=\"1\" $SERVER/$APPNAME:$TAG"

# docker login -u deptha -p bXI91q30LPB5 192.168.107.22
# docker push $SERVER/$APPNAME:$TAG

# notify-send "punten" "deploy dulu"

# ssh root@192.168.24.63 "
#     docker pull $SERVER/$APPNAME:$TAG;
#     docker rm -f $APPNAME-1;
#     docker container run -d --env-file /home/ws/catalog-creator/.env1 --name $APPNAME-1 --restart always --log-opt max-size=50m -m 1g --cpus=\"1\" $SERVER/$APPNAME:$TAG -m scheduling -p online;
#     docker rm -f $APPNAME-2;
#     docker container run -d --env-file /home/ws/catalog-creator/.env2 --name $APPNAME-2 --restart always --log-opt max-size=50m -m 1g --cpus=\"1\" $SERVER/$APPNAME:$TAG -m scheduling -p online;
# "

# # docker container run -d --env-file /home/deptha/eBdesk/project/custom_request/catalog-creator/.env --name catalog-creator-1 --restart always --log-opt max-size=50m -m 1g --cpus=1 192.168.107.22/imav2/catalog-creator:1.0.0 \ -m scheduling 