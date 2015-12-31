REGISTRY_BASE ?= markbnj
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

clean-base:
	rm -f base/image-build.log
	($(DOCKER_IMAGE_LIST) | awk '$$NF == "$(REGISTRY_BASE)/jobber-base"') || $(DOCKER_RMI) $(REGISTRY_BASE)/jobber-base

clean-jobber:
	rm -f jobber/image-build.log
	rm -rf jobber/temp
	($(DOCKER_CONTAINER_LIST) | awk '$$NF == "$(IMAGE_NAME)" {exit 1}') || $(DOCKER_RM) $(IMAGE_NAME)
	($(DOCKER_IMAGE_LIST) | awk '$$NF == "$(REGISTRY_BASE)/$(IMAGE_NAME)"') || $(DOCKER_RMI) $(REGISTRY_BASE)/$(IMAGE_NAME)

base-image:
	$(DOCKER_BUILD) --tag=$(REGISTRY_BASE)/jobber-base:$(TAG) --rm=true --force-rm=true base | tee base/image-build.log

jobber-image:
	curl -H "Authorization: token $(GITHUB_TOKEN)" -L https://api.github.com/repos/markbnj/jobber/tarball/master -o jobber/jobber.tar.gz
	mkdir jobber/temp
	cd jobber/temp && tar -xzf ../jobber.tar.gz --strip-components=1
	rm jobber/jobber.tar.gz
	$(DOCKER_BUILD) --tag=$(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG) --rm=true --force-rm=true jobber | tee jobber/image-build.log

build: clean-jobber jobber-image

build-all: clean-base base-image clean-jobber jobber-image

run:
	($(DOCKER_CONTAINER_LIST) | awk '$$NF == "$(IMAGE_NAME)" {exit 1}') || $(DOCKER_RM) $(IMAGE_NAME)
	$(DOCKER_RUN) -h $(IMAGE_NAME) --name=$(IMAGE_NAME) -p 5000:5000 -p 5010:5010 $(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG)