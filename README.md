# Convert jaeger data to influx-data
```sh
docker run --net=host --volume (pwd):/backup influxdb:1.8
```

```sh
docker exec -it <influx_container_name> /bin/bash

# run inside docker 

influx 

CREATE DATABASE "jaeger-traces"
```

### open this project inside a python docker container

```sh
docker run -v (pwd):/my-influx --net=host -it python:3.12.0 bash

# run these cmd inside docker 

pip install -r requirements.txt

python main.py
```

### to export influxdb data to csv
```sh

docker exec -it <influx_container_name> /bin/bash

# export to current directory location

influx -database jaeger-traces -execute 'select * from spans' -format csv > ./exported-jaeger-traces.csv
```
