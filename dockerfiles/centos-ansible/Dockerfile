FROM centos:8

RUN yum clean all \
    && yum -y install epel-release \
    && yum -y install PyYAML python-jinja2 python-httplib2 python-keyczar python-paramiko python-setuptools git python-pip \
	&& mkdir /etc/ansible/ \
    && echo -e '[local]\nlocalhost' > /etc/ansible/hosts \
    && pip install ansible