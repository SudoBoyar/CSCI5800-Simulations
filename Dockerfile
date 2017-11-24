FROM jupyter/scipy-notebook
WORKDIR /home/jovyan/work
RUN pip install simpy PyQt5
ADD . /home/jovyan/work
CMD ["python", "craps.py"]