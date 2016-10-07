from frolvlad/alpine-python3

# Install dependencies
RUN pip install wit \
 && pip install PyYaml \
 && pip install -U flask-cors

ADD . /alquist

WORKDIR /alquist

CMD ["python3", "main.py"]

# Expose port
EXPOSE 5000

