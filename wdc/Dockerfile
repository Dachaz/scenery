FROM fedora:latest

RUN yum -y install \
    glibc.i686 \
    libxml2 \
    libxml2-devel \
    libxml2.i686 \
    libxml2-devel.i686 \
    tar \
    openssl \
    unzip

# Get the proprietary mksapkg binary from WDC
RUN curl https://developer.westerndigital.com/content/dam/developer-portal/external/sdk/my-cloud/mksapkg-64b.zip -O && \
    unzip mksapkg-64b.zip && \
    mv mksapkg-64b /usr/local/bin/mksapkg && \
    chmod +x /usr/local/bin/mksapkg

WORKDIR /usr/src/scenery

ADD ./src /usr/src/scenery

ENTRYPOINT chmod +x /usr/src/scenery/*.sh && \
    chmod +x /usr/src/scenery/app/scenery-bin && \
    mksapkg -E -s -m WDMyCloudMirrorGen2 && \
    cd .. && \
    mv *scenery*.bin* /build
