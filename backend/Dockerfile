FROM condaforge/miniforge3

WORKDIR /app

COPY environment.yml ./
COPY src ./src

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

ENTRYPOINT ["bash", "-c", "cd src/main && python main.py"]
