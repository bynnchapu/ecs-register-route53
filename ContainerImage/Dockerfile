FROM amazonlinux:2.0.20210617.0

RUN yum -y install python3 && \
    pip3 install boto3
ADD register-route53.py /usr/local/bin/

ENTRYPOINT /usr/bin/python /usr/local/bin/register-route53.py