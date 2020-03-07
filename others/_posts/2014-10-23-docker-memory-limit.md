---
layout: single
title: Docker memory limit
---

I was playing with how Docker’s memory limit works, and found something very odd.

Docker advertises that, you can set the maximum memory size that the docker container can use by setting –memory option like this.

```bash
docker run -it --rm --memory 2000M centos
```

To see what it does, I’ve written a small python script that creates a long string.

```python
print "allocating 3G"
some_str = ' '*1024*1024*1024*3
print "ok"
```

And a Dokerfile

```
FROM node
ADD test.py .
```

```bash
docker build -t soichih/memorylimit .
```

And here is the result

```bash
$ docker run -it --rm --memory 2000M soichih/memorylimit
allocating 3G
Killed

$ echo $?
137
```

137 == kill 9. So, it looks like Docker/LXC was able to kill my docker process when it reached the 2000M memory limit.. I’ve also tried running my test.py inside another shell script to see if Docker/LXC will monitor memory usage of child process, and it did. So far so good.

Now, what happen if I start up multiple child processes? Will Docker/LXC calculate the aggregate memory usage and kill both processes?

I’ve updated my test.py to the following

```python
some_str0 = ' '*1024*1024*500
print "allocated 500M"
some_str1 = ' '*1024*1024*500
print "allocated 1000M"
print "done"
```

I then updated my test script to following.

```bash
./test.py &
./test.py &
echo "sleeping 30 seconds"
sleep 30
```

The idea here is that, I will be running 2 test.py that each will consume up to 1G (totalling 2G) I will set –memory 1000M in a hope that, by the time each test.py will consume the first 500M, both process will be killed.. So let’s see.

```bash
$ docker run -it --rm --memory 1000M soichih/memorylimit
sleeping 30 seconds
allocated 500M
allocated 500M
allocated 1000M
done allocating
allocated 1000M
done allocating
```

So.. what's happening here? It looks like Docker/LXC doesn't kill my container, even though the container as a whole has allocated 2G total. I’ve tried it with 3G, 4G, 5G in total, but the results were the same. Docker will only kill individual process that consumes more than specified amount of memory (according to -memory), but you can still run as many processes inside the container as you want, and Docker will happily let you run them.

Maybe I am completely misunderstanding how -memory options works, or how python allocates its memory, but as far as I know this is not the way I expect -memory to work.

For more info..
> https://github.com/docker/docker/issues/8769
