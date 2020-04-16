FROM centos:7
MAINTAINER Tatiana Hanazaki <tatiana.hana@equinox.com>

# dependency install
RUN yum -y install epel-release && \
    yum -y install https://centos7.iuscommunity.org/ius-release.rpm && \
    yum -y install python36 && \
    yum -y install python36-pip && \
    yum -y install python36-devel && \
    yum -y install git && \
    yum -y install npm && \
    yum -y install nginx && \
    yum clean all

RUN localedef -i en_US -f UTF-8 C.UTF-8
ENV LANG="C.UTF-8"
ENV LC_LANG="C.UTF-8"

# build arguments
    ARG aws_access_key_id
    ARG aws_secret_access_key
    ARG config_path
    ARG public_url

#clone repos
WORKDIR /usr/local/
RUN git clone https://github.com/Bubbassauro/runduck.git runduck && \
    git clone https://github.com/Bubbassauro/runduck-ui.git runduck-ui && \
    #copy config file from s3
    pip3.6 install awscli && \
    mkdir /root/.aws/ && \
    echo [default] >> /root/.aws/credentials && \
    echo aws_access_key_id = $aws_access_key_id >> /root/.aws/credentials && \
    echo aws_secret_access_key = $aws_secret_access_key >> /root/.aws/credentials && \
    echo [default] >> /root/.aws/config && \
    echo region = us-east-1 >> /root/.aws/config && \
    aws s3 cp s3://eqxdl-prod-support/devops-ssh/id_rsa ~/.ssh/id_rsa && \
    chmod 400 ~/.ssh/id_rsa && \
    ssh -o "StrictHostKeyChecking=no" git@bitbucket.org && \
    aws s3 cp $config_path/app.cfg /usr/local/runduck/app.cfg && \
    aws s3 cp $config_path/nginx.conf /etc/nginx/nginx.conf

# Install requirements for the backend
RUN cd /usr/local/runduck && \
    pip3.6 install -r requirements.txt && \
    pip3.6 install gunicorn

# Install node, build frontend part with the correct paths (public_url)
# copy the UI build to the application folder
RUN curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo && \
    rpm --import https://dl.yarnpkg.com/rpm/pubkey.gpg && \
    npm cache clean -f && \
    npm install -g n && \
    n stable && \
    yum -y install yarn && \
    export PUBLIC_URL=$public_url && \
    cd /usr/local/runduck-ui && \
    yarn install && \
    yarn build && \
    yes | cp -rf build /usr/local/runduck

EXPOSE 3825

WORKDIR /usr/local/runduck
CMD nginx; gunicorn -b :80 runduck:app