FROM wghilliard/lar_root:latest
MAINTAINER grsn.hilliard@gmail.com
COPY get-pip.py /opt/
COPY requirements.txt /opt/
COPY presets /products/presets

RUN source /opt/root/bin/thisroot.sh && cd /opt/ && python get-pip.py && pip install -r requirements.txt

