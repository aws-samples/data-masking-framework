FROM datamask

RUN . scripts/activate_venv.sh && \
    .venv/bin/pip install jupyter sparksql-magic
CMD . scripts/activate_venv.sh && PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook --allow-root --ip 0.0.0.0 --port 8888" $PYTHONPATH/pyspark/bin/pyspark  $*

	

