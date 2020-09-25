# Prerequisite

- Make scripts executable
```bash
chmod +x ./start.sh && \
chmod +x ./run_user_sim.sh && \
chmod +x ./stop.sh
```

# 1. Start microservices demo

The __start.sh__ script starts (and builds) all the necessary docker containers for microservices, monitoring and logging.

# 2. Simulating user behavior

To simulate the user behavior run the __run\_user\_sim.sh__ script.

# 3. Shutting down containers

To close all the running containers simply run the __stop.sh__ script.

# Port forwarding

The following script forwards all the ports from the server to the local machine:

```bash
ssh -N -f -L localhost:8080:localhost:80 \
          -L localhost:3000:localhost:3000 \
          -L localhost:5601:localhost:5601 \
          -L localhost:9090:localhost:9090 \
             petar@wally113.cit.tu-berlin.de

```

# Urls:
- __Grafana__ - localhost: 3000 
  - __user__:admin
  - __password:__ foobar
- __Sockshop__ - localhost:8080 or localhost
- __Prometheus__ - localhost:9090
- __Kibana__ - localhost:5601

# Prometheus to CSV
```bash
python3 scrape_logs.py http://localhost:9090

```
The results are stored in metrics.csv

# Elasticsearch to csv
To create the query, edit the __query.json__ timestamps!


```bash
es2csv -q es2csv -u http://localhost:9200 -e -f _all -r -q @'query.json' -o csv_raw.csv --debug

```
The results are stored in csv_raw.csv



pumba netem --duration 2m --tc-image gaiadocker/iproute2 delay --time 200 "re2:^microservices"
pumba netem --duration 2m loss --time 200 re2:microservices