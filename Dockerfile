# ----------------------------
# Base Image
# ----------------------------
FROM python:3.10-slim

# ----------------------------
# Set Working Directory
# ----------------------------
WORKDIR /app

# Copy Requirements First (for caching)
# ----------------------------
COPY requirements.txt .

# ----------------------------
# Install Python Dependencies
# ----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Copy Project Files
# ----------------------------
COPY . .

# ----------------------------
# Create Logs Directory
# ----------------------------
RUN mkdir -p logs

# ----------------------------
# Run Application
# ----------------------------
CMD ["python", "run.py"]