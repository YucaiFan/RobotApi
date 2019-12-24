# RobotApi
## Uploading Files:
```curl http://localhost:5000/testupload -F "file=@/RobotApi/data/examples/kawada-hironx.zae" -v```
```curl http://localhost:5000/api/robot -F "file=@/RobotApi/data/examples/kawada-hironx.zae" -v```
```curl http://localhost:5000/api/robot -F "file=@/collada_robots/kuka-kr150.zae" -v ```

## Deleting Files:
```curl -v -X DELETE http://localhost:5000/api/robot/kawada-hironx.zae```

## Geting and Downloading:
```curl -i http://localhost:5000/api/robot/kawada-hironx/download```
```curl -i http://localhost:5000/api/robot/kawada-hironx
curl -i http://localhost:5000/api/robot/```
