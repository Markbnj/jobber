REGISTRY_BASE ?= markbnj
BASE_IMAGE = debian\:wheezy
IMAGE_NAME ?= jobber
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
TAG ?= $(subst /,-,$(BRANCH))
GITHUB_TOKEN ?= 0b14ea13c508b3083d142e5dc771a2c793641707
DOCKER_BUILD ?= docker build
DOCKER_PUSH ?= docker push
DOCKER_RUN ?= docker run -it
DOCKER_CONTAINER_LIST ?= docker ps -a
DOCKER_RMI ?= docker rmi
DOCKER_RM ?= docker rm -f

clean:
	rm -f .docker/Dockerfile
	rm -f image-build.log
	rm -f .docker/jobber.tar.gz
	rm -rf .docker/jobber
	($(DOCKER_CONTAINER_LIST) | awk '$$NF == "$(IMAGE_NAME)" {exit 1}') || $(DOCKER_RM) $(IMAGE_NAME)
	$(DOCKER_RMI) $(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG)

build: clean container

container:
	sed -e"s:##BASE##:$(BASE_IMAGE):g" .docker/Dockerfile.template > .docker/Dockerfile
	curl -H "Authorization: token $(GITHUB_TOKEN)" -L https://api.github.com/repos/markbnj/jobber/tarball/master -o .docker/jobber.tar.gz
	mkdir .docker/jobber
	cd .docker/jobber && tar -xzf ../jobber.tar.gz --strip-components=1
	$(DOCKER_BUILD) --tag=$(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG) --rm=true --force-rm=true .docker | tee image-build.log

run:
	$(DOCKER_RUN) -h $(IMAGE_NAME) --name=$(IMAGE_NAME) $(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG)