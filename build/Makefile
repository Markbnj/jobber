DOCKER_BUILD = docker build
DOCKER_PUSH = docker push
REGISTRY_BASE = markbnj
BASE_IMAGE = debian\:wheezy
IMAGE_NAME = jobber
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
TAG = $(subst /,-,$(BRANCH))

clean:
	rm -f .docker/Dockerfile
	rm -f image-build.log

build: clean container

container:
	sed -e"s:##BASE##:$(BASE_IMAGE):g" .docker/Dockerfile.template > .docker/Dockerfile
	$(DOCKER_BUILD) --tag=$(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG) --rm=true --force-rm=true .docker | tee image-build.log
