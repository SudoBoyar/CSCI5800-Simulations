FROM jupyter/scipy-notebook
WORKDIR /home/jovyan/work
RUN pip install simpy
ADD . /home/jovyan/work
CMD ["tini", "--", "start-notebook.sh"]