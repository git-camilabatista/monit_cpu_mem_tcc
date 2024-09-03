# 📌 CPU and Memory Consumption Monitoring with Sysstat

1. Clone this project into your preferred directory:

```sh
git clone git@github.com:git-camilabatista/monit_cpu_mem_tcc.git
```

2. Navigate to the `monit_cpu_mem_tcc` directory that was created:

```sh
cd monit_cpu_mem_tcc
```

3. Run the command to install all the necessary dependencies:

> [!IMPORTANT]
> To proceed with this step, it is necessary to have [Poetry](https://python-poetry.org/) already installed.

```sh
poetry install
```

4. Find the PID related to the running application:

> [!IMPORTANT]
> Before starting the CPU and memory monitoring test, remember to launch the application that will be analyzed.

```sh
htop
```

5. Run the command to start the monitoring service:

```sh
pidstat -r -u -p <PID> <log_interval> log_file_name.log
```

* -r: Collect memory consumption data.
* -u: Collect CPU usage data.
* -p <PID>: Set the PID to be monitored.
* log_interval: Set the time interval between each entry recorded by sysstat in the log file.
