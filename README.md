# ![RealWorld Example App](logo.png)

FastAPI codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld-example-apps) spec and API.

## [RealWorld](https://github.com/gothinkster/realworld)

This codebase was created to demonstrate a fully fledged fullstack application built with FastAPI including CRUD operations, authentication, routing, pagination, and more.

We've gone to great lengths to adhere to the Python community styleguides & best practices.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.

## Usage

### PostgreSQL

This project use **PostgreSQL** as main database provider. You can run it easily via `docker-compose up -d`.

Two databases will spin up, one for normal development and one dedicated for integrations tests.

### Run app

```sh
pipenv install # install dependencies
cp .env.example .env # access for above container
make migrate # alembic migration
make seed # fake data with faker
make run # run uvicorn
```

And that's all, go to <http://localhost:8000/docs>

### Validate API with Newman

Launch follow scripts for validating realworld schema :

```sh
make fresh # wipe all database for clean state
make run
npx newman run postman.json --global-var "APIURL=http://localhost:8000/api" --global-var="USERNAME=johndoe" --global-var="EMAIL=john.doe@example.com" --global-var="PASSWORD=password"
```

### Full test suite

This project is fully tested via pytest, just run `pytest` for launching it.

## License

This project is open-sourced software licensed under the [MIT license](https://adr1enbe4udou1n.mit-license.org).
