---
layout: single
title: Installing perfSONAR / Central MA (aka esmond) via Docker
published: true
---

It's quite trivial to install perfSONAR meshconfig admin with docker.

### Step 1) Start cassandra / pstgres container (if you don't have one)

```bash
docker run --name esmond-cassandra1 \
    --restart=always \
    -d cassandra:2.1

docker run --name esmond-postgres1 \
    --restart=always \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -d postgres
```

### Step 2) Start esmond

```
docker run --name esmond1 \
--restart=always \
--link esmond-postgres1:postgres \
--link esmond-cassandra1:cassandra \
-p 80:80 \
-d soichih/esmond
```

### Step 3) Grab the esmond API key from the log

Unfortunately, esmond doesn't let you specify apikey before you star the container. It *generates* one for you, so you have to grab it from the log after you start it up.

```
$ docker logs esmond1
...
Key: dc2c3e7869f6b02f5a9ddfd21c49ca8c32c241f2 for perfsonar
...
```

That's it! Now you can place your esmond behind a proxy, or make it part of your infrastructure by configuring your measurement hosts, etc.. (<a href="http://docs.perfsonar.net/multi_central_MA.html" target="_blank">See</a>)

On my setup, I expose the esmond's port 80 as Docker host's port 8092, and I have following in my nginx configuration to expose it through my proxy's port 80 on /esmond URL.

```
location /esmond/ {
    proxy_pass http://localhost:8092;
}
```

For a list of versions available, see https://hub.docker.com/r/soichih/esmond/tags/ (right now I've only built esmond-1.0.16). I will post Dockerfile and other bootstrap scripts after I confirm that everything works.
