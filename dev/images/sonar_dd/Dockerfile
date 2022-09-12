FROM ubuntu:20.04

RUN apt update -y
RUN apt install git -y
RUN apt install -y python3 python3-pip
RUN usermod -s /usr/sbin/nologin root
RUN adduser sidecar
RUN mkdir /results
VOLUME /results
COPY ./dd_sonar.py ./
RUN chown -R sidecar /results
RUN chown -R sidecar /dd_sonar.py
USER sidecar
RUN pip3 install requests_toolbelt pyyaml requests
RUN chmod +x /dd_sonar.py
ENTRYPOINT [ "/usr/bin/python3", "/dd_sonar.py" ]
