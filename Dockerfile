from frolvlad/alpine-python3

# Install dependencies
RUN pip install wit \
 && pip install PyYaml \
 && pip install -U flask-cors

ADD . /alquist

WORKDIR /alquist

# Expose port
EXPOSE 5000

