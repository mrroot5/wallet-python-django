# Django atomic transactions
This project simulate a virtual wallet to use Django atomic transactions.

## Requirements

* docker engine >= 19.03.
* docker-compose >= 1.27.

## Tested on

* Ubuntu 18.04 (Bionic).
* docker engine == 20.10.9.
* docker-compose == 1.28.4.

## Relational models image

[Graph model image](docs/images/graph-models.png)

## Build project

## How to run project this project?

### Using make command (recommended)

If you can run a `Makefile` command, you can use a "fast init" with: `make loaddata`.

### Build

Build docker image:

```shell
make build
```

#### Migrate

Apply django migrations:

```shell
make migrate
```

#### Runserver

Run django runserver command:

```shell
make dev
```

#### Uvicorn

Run uvicorn server:

```shell
make web
```

#### Load sample data

Apply `initial_data.json` fixture:

```shell
make loaddata
```

### Using docker-compose

#### Step 1: Build

```shell
docker-compose -p django_atomic_transactions -f environment/docker-compose.yml build
```

#### Step 2: Migrate

Apply django migrations:

```shell
docker-compose -p django_atomic_transactions -f environment/docker-compose.yml run --rm --service-ports web migrate
```

#### Step 3: Run service

* **Runserver**

Run django runserver command:

```shell
docker-compose -p django_atomic_transactions -f environment/docker-compose.yml run --rm --service-ports web dev
```

* **Uvicorn**

Run uvicorn server:

```shell
docker-compose -p django_atomic_transactions -f environment/docker-compose.yml run --rm --service-ports web web
```

#### Step 4: Load sample data

Apply `initial_data.json` fixture:

```shell
docker-compose -p django_atomic_transactions -f environment/docker-compose.yml run --rm --service-ports web loaddata
```

## TODO

* Finish Dockerfile production stage.
