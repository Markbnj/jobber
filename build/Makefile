REGISTRY_BASE ?= markbnj
IMAGE_NAME ?= jobber
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
TAG ?= $(subst /,-,$(BRANCH))
DOCKER_BUILD ?= docker build
DOCKER_PUSH ?= docker push
DOCKER_RUN_DEBUG ?= docker run -it
DOCKER_RUN ?= docker run -d
DOCKER_CONTAINER_LIST ?= docker ps -a
DOCKER_IMAGE_LIST ?= docker images
DOCKER_RMI ?= docker rmi
DOCKER_RM ?= docker rm -f

export TEST_HOST ?= localhost
export API_TEST_PORT ?= 5000
export ADMIN_TEST_PORT ?= 8080

clean-base:
	rm -f base/image-build.log
	($(DOCKER_IMAGE_LIST) | awk '$$NF == "$(REGISTRY_BASE)/jobber-base"') || $(DOCKER_RMI) $(REGISTRY_BASE)/jobber-base

clean-jobber:
	rm -f jobber/image-build.log
	rm -rf jobber/code
	($(DOCKER_CONTAINER_LIST) | awk '$$NF == "$(IMAGE_NAME)" {exit 1}') || $(DOCKER_RM) $(IMAGE_NAME)
	($(DOCKER_IMAGE_LIST) | awk '$$NF == "$(REGISTRY_BASE)/$(IMAGE_NAME)"') || $(DOCKER_RMI) $(REGISTRY_BASE)/$(IMAGE_NAME)

base-image:
	$(DOCKER_BUILD) --tag=$(REGISTRY_BASE)/jobber-base:$(TAG) --rm=true --force-rm=true base | tee base/image-build.log

jobber-image:
	mkdir jobber/code
	cp -Rf ../jobber/* jobber/code/
	$(DOCKER_BUILD) --tag=$(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG) --rm=true --force-rm=true jobber | tee jobber/image-build.log

stop:
	($(DOCKER_CONTAINER_LIST) | awk '$$NF == "$(IMAGE_NAME)" {exit 1}') || $(DOCKER_RM) $(IMAGE_NAME)

run: stop
	$(DOCKER_RUN) -h $(IMAGE_NAME) --name=$(IMAGE_NAME) -p $(API_TEST_PORT):$(API_TEST_PORT) -p $(ADMIN_TEST_PORT):$(ADMIN_TEST_PORT) $(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG)

run-debug: stop
	$(DOCKER_RUN_DEBUG) -h $(IMAGE_NAME) --rm=true --name=$(IMAGE_NAME) -p $(API_TEST_PORT):$(API_TEST_PORT) -p $(ADMIN_TEST_PORT):$(ADMIN_TEST_PORT) $(REGISTRY_BASE)/$(IMAGE_NAME):$(TAG) /usr/local/bin/jobber/start-jobber.sh -d

.run-test:
	cd ../ && nosetests -v -w jobber/tests/

test: run .run-test stop

build: clean-jobber jobber-image test

build-all: clean-base base-image clean-jobber jobber-image test
