FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

COPY conda-linux-64.lock /tmp/conda-linux-64.lock

USER root

# Install lmodern for Quarto PDF rendering
RUN apt-get update \
    && apt-get install -y --no-install-recommends lmodern \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Update and clean Conda packages, handle permissions
RUN mamba update --quiet --file /tmp/conda-linux-64.lock || echo "mamba update encountered an issue" \
    && mamba clean --all -y -f \
    && chown -R $NB_UID:$NB_GID "${CONDA_DIR}" \
    && chown -R $NB_UID:$NB_GID "/home/${NB_USER}" \
    && chmod -R u+rwx "/home/${NB_USER}"

# Install required Python package
RUN pip install deepchecks==0.18.1

# Switch back to non-root user
USER $NB_UID

