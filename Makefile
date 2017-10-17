HOST_PATH ?= $(shell pwd)

REPO_ORG ?= $(shell basename $(HOST_PATH))
REPO = $(shell echo $(REPO_ORG) | tr A-Z a-z)

TAG = 'develop'

GUEST_PATH = '/tmp/$(REPO)'

CMD_DEV = 'cd $(GUEST_PATH) && /bin/bash restart-service.sh && /bin/bash'
CMD_TEST = 'cd $(GUEST_PATH) && /bin/bash run-test.sh'

HOST_PORT ?= 80

build: Dockerfile
	docker build \
	  -t $(REPO):$(TAG) -f Dockerfile .

run:
	docker run --rm \
	  -v $(HOST_PATH):$(GUEST_PATH) \
      -v $(HOST_PATH)/config:/tmp/config \
      -v $(HOST_PATH)/config/nginx-myws.conf:/etc/nginx/conf.d/nginx-myws.conf \
	  -p $(HOST_PORT):80 \
	  $(DOCKER_OPTIONS) -it $(REPO):$(TAG) /bin/bash -c $(CMD_DEV)

test:
	docker run --rm \
	  -v $(HOST_PATH):$(GUEST_PATH) \
      -v $(HOST_PATH)/config:/tmp/config \
      -v $(HOST_PATH)/config/nginx-myws.conf:/etc/nginx/conf.d/nginx-myws.conf \
	  $(DOCKER_OPTIONS) -it $(REPO):$(TAG) /bin/bash -c $(CMD_TEST)

