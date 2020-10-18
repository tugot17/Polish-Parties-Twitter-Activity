#By  @burnpiro
FROM jupyter/scipy-notebook

ARG conda_env=python36
ARG py_ver=3.6

RUN conda create --quiet --yes -p $CONDA_DIR/envs/$conda_env python=$py_ver ipython ipykernel && \
    conda clean --all -f -y

RUN $CONDA_DIR/envs/${conda_env}/bin/python -m ipykernel install --user --name=${conda_env} && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

ENV PATH $CONDA_DIR/envs/${conda_env}/bin:$PATH

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN git clone --depth=1 https://github.com/himanshudabas/twint.git && \
    cd twint && \
    pip install . -r requirements.txt

ENV WORK_DIR ${HOME}/work
USER jovyan

RUN python --version