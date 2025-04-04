# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install make utility
RUN apt-get update && apt-get install -y make && apt-get clean

# Copy the entire project into the container
COPY . .

# Install dependencies using the Makefile
RUN make install

# Expose the gRPC server port
EXPOSE 50051

# Command to run the server using the Makefile
CMD ["make", "run"]