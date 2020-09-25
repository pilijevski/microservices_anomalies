import os
from base import Runnable
from datetime import datetime


class UserSim(Runnable):
    def __init__(self, cconfig, simconfig, timeout=0, name="user_sim"):
        self.name = name
        self.timeout = timeout
        self.cconfig = cconfig
        self.simconfig = simconfig
        self.exec_string = self.parse_exec_string()

    def parse_exec_string(self):
        return "docker run " \
               "--rm -d --network microservices-network " \
               f"--hostname {self.cconfig.hostname} " \
               f"--name {self.cconfig.name} " \
               f"weaveworksdemos/load-test:0.1.1 " \
               f"-d {self.simconfig.delay} -r {self.simconfig.requests} " \
               f"-c {self.simconfig.clients} -h {self.simconfig.host}"

    def run(self):
        print(f"{datetime.utcnow()}")
        return self.run_user_sim()

    def run_user_sim(self):
        os.system(self.exec_string)
        return self
