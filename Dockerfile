from python:3

# Install dependencies
RUN pip install wit \
 && pip install PyYaml \
 && pip install -U flask-cors \
 && pip install bs4 \
 && pip install ufal.morphodita

ADD . /alquist

WORKDIR /alquist

CMD ["python3","-u", "main.py"]

# Expose port
EXPOSE 5000

