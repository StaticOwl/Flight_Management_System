FROM condaforge/miniforge3:latest

WORKDIR /app

# Copy environment.yml file and requirements.txt
COPY environment.yml ./
COPY requirements.txt ./

# Create conda environment
RUN conda env create -f environment.yml

# Make RUN commands use the new environment and install Flask and other requirements
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN pip install -r requirements.txt
RUN pip install flask

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set up proper Python path to find modules
ENV PYTHONPATH=/app:/app/src

# Command to run the application
CMD ["conda", "run", "--no-capture-output", "-n", "base", "python", "/app/src/main/app.py"]