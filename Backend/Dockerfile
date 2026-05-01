#Version 1
# FROM python:3.12-slim

# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# #Figure out why uvicorn is not being installed with the requirements.txt file. For now, we will install it separately.
# RUN pip install uvicorn

# COPY src/mysite mysite

# EXPOSE 8000

# CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "8000"]

#Version 2 (with builder and runner stages)
FROM python:3.12-slim AS builder

WORKDIR /app
#Make python install the dependencies and create wheel files for them. This will speed up the installation process in the runner stage.
#Also make python project installable by including the pyproject.toml file. This will allow us to install the project as a package (other wheels will not work) in the runner stage, which will also speed up the installation process.
#pip wheel is akin to a glorified zip file (a prebuilt, installable Python package). It will create a wheel file for each dependency in the requirements.txt file and for the project itself. The --no-deps flag is used to prevent pip from installing the dependencies of the dependencies, which will save time and space in the image. The --wheel-dir flag is used to specify the directory where the wheel files will be stored.
COPY pyproject.toml requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

#copy the source code of the application in the builder stage and create a wheel file for it. This will allow us to install the application as a package in the runner stage, which will speed up the installation process and reduce the size of the image.
COPY src src
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

#Now we will create the runner stage. This stage will be used to run the application. We will copy the wheel files from the builder stage and install them in this stage. We will also copy the source code of the application in this stage and install it as a package.
FROM python:3.12-slim AS runner

#Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
#install the dependencies from the wheel files and then remove the wheel files to save space in the image. All within one layer to minimize the number of layers in the image.
#Another benefit is potentially squashing creates and deletes which cancel one another out, which can further reduce the image size.
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

#The runner now has no build dependencies and only the runtime dependencies, which will significantly reduce the image size.
#We simply installed the productions wheels. The builder stage can have all the build dependencies, which can be quite large, without affecting the size of the final image.

EXPOSE 8000

CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "8000"]

#To target a specific stage in the build process, we can use the --target flag with the docker build command. For example, to build only the builder stage, we can run:
#docker build --target builder -t myapp-builder . This will build only the builder stage and create an image with the tag myapp-builder. We can then use this image to run the builder stage and create the wheel files without having to build the entire image. This can be useful for debugging or for creating a cache of the wheel files that can be reused in subsequent builds.

#We could also build mulitple stages and create multiple images in one build. For example, we could build both the builder and runner stages and create two images with the tags myapp-builder and myapp-runner. We can then use these images to run the builder and runner stages separately. This can be useful for testing or for creating different versions of the application with different configurations.
#docker command: docker build -t mysite-backend -f dev.dockerfile .