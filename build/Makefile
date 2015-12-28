REGISTRY_BASE ?= markbnj
BASE_IMAGE = debian\:wheezy
IMAGE_NAME ?= jobber
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
TAG ?= $(subst /,-,$(BRANCH))
DOCKER_BUILD ?= docker build
DOCKER_PUSH ?= docker push
DOCKER_RUN ?= docker run -it
DOCKER_CONTAINER_LIST ?= docker ps -a
DOCKER_IMAGE_LIST ?= docker images
DOCKER_RMI ?= docker rmi
DOCKER_RM ?= docker rm -f

include gh_token.mk

clean:
	rm -f jobber/Dockerfile
	rm -f jobber/image-build.log
	rm -f jobber/jobber.tar.gz
	rm -rf jobber/temp
	($(DOCKER_CONTAINER_LIST) | awk '$$NF == "$(IMAGE_NAME)" {exit 1}') || $(DOCKER_RM) $(IMAGE_NAME)
	($(DOCKER_IMAGE_LIST) | awk '$$NF == "$(REGISTRY_BASE)/$(IMAGE_NAME)"') || $(DOCKER_RMI) $(REGISTRY_BASE)/$(IMAGE_NAME)

build: clean container

container:
	sed -e"s:##BASE##:$(BASE_IMAGE):g" jobber/Dockerfile.template > jobber/Dockerfile
	curl -H "Authorization: token $(GITHUB_TOKEN)" -L https://api.github.com/repos/markbnj/jobber/tarball/master -o jobber/jobber.tar.gz
	mkdir jobber/temp
	cd jobber/temp && tar -xzf ../jobber.tar.gz --strip-components=1
	$(DOCKER_BUILD) --tag=$(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG) --rm=true --force-rm=true jobber | tee jobber/image-build.log

run:
	$(DOCKER_RUN) -h $(IMAGE_NAME) --name=$(IMAGE_NAME) $(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG)