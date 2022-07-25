docker build --pull --rm -f "dockerfile" -t torplus_stellar:latest "."
docker run --name torplus_stellar --rm -i -t torplus_stellar bash