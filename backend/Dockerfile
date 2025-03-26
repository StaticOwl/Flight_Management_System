FROM condaforge/miniforge3:latest

WORKDIR /app

COPY environment.yml ./

# Create conda environment and activate it
RUN conda env create -f environment.yml && \
    echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" >> ~/.bashrc

# Ensure the conda environment is activated in non-interactive shells
SHELL ["/bin/bash", "--login", "-c"]

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set up proper Python path to find modules
ENV PYTHONPATH=/app:/app/src

# Command to run the application
CMD ["conda", "run", "--no-capture-output", "-n", "flights", "python", "/app/src/main/app.py"]
