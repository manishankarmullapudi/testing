FROM ubuntu:20.04

RUN apt update -y
RUN apt install -y dpkg wget curl
# Change permission to execute the shell script before building the image as the same permissions are carried over into the image
COPY ./octant_downloader.sh ./
RUN sed -i 's/\r//g' octant_downloader.sh
RUN chmod +x ./octant_downloader.sh
RUN ./octant_downloader.sh
RUN rm /octant_downloader.sh
RUN dpkg -i octant.deb
RUN rm octant.deb


EXPOSE 7777
RUN mkdir /kubeconfig
VOLUME /kubeconfig 

RUN adduser --disabled-login --quiet octant && chown -R octant /kubeconfig
RUN usermod -s /usr/sbin/nologin root

COPY ./starboard_octant_plugin.sh /home/octant/starboard_octant_plugin.sh
RUN chown -R octant /home/octant/starboard_octant_plugin.sh
USER octant
RUN chmod +x /home/octant/starboard_octant_plugin.sh
RUN mkdir -p /home/octant/.config/octant/plugins
RUN sed -i 's/\r//g' /home/octant/starboard_octant_plugin.sh
WORKDIR /home/octant/
RUN /home/octant/starboard_octant_plugin.sh

ENV OCTANT_LISTENER_ADDR=0.0.0.0:7777
ENV KUBECONFIG=/kubeconfig/config
HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:7777/ || exit 1
#--restart unless-stopped --> always add this flag for running this container
ENTRYPOINT [ "/usr/local/bin/octant", "--disable-open-browser", "--disable-origin-check" ]
