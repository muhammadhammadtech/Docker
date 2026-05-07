# Base image with Jupyter notebook
FROM jupyter/base-notebook:latest

# Metadata labels (industry best practice)
LABEL maintainer="mehmed" \
      description="Jupyter notebook with ML packages installed" \
      version="1.0" \
      license="MIT" \
      org.opencontainers.image.source="https://github.com/yourusername/ml-docker"

# Switch to root to install packages
USER root

# Install ML packages in a single layer and reduce image size
RUN pip install --no-cache-dir \
        tensorflow==2.14 \
        scikit-learn==1.3 \
        pandas==2.1 \
        numpy==1.26 \
        matplotlib==3.8 \
        seaborn==0.13 \
        joblib==1.3

# Switch back to non-root user for security
USER jovyan

# Expose Jupyter notebook port
EXPOSE 8888

# Default command to start Jupyter notebook
CMD ["start-notebook.sh"]
