# Superheroes API

## Overview

This API tracks heroes and their superpowers. 
It supports CRUD operations for `Hero`, `Power`, and `HeroPower` models and provides endpoints to manage these entities.

## Models

### Hero

- `id`: Integer, Primary Key
- `name`: String, required
- `super_name`: String, required

### Power

- `id`: Integer, Primary Key
- `name`: String, required
- `description`: String, required, at least 20 characters long

### HeroPower

- `id`: Integer, Primary Key
- `strength`: String, required, one of `Strong`, `Weak`, `Average`
- `hero_id`: Foreign Key to `Hero`
- `power_id`: Foreign Key to `Power`

## Endpoints

### GET /api/heroes
Returns a list of all heroes.

### GET /api/heroes/:id
Returns a specific hero by ID, including their powers.

### GET /api/powers
Returns a list of all powers.

### GET /api/powers/:id
Returns a specific power by ID.

### PATCH /api/powers/:id
Updates a power's description. The description must be at least 20 characters long.

### POST /api/hero_powers
Creates a new HeroPower association. The strength must be one of `Strong`, `Weak`, or `Average`.

## Setup

1. Clone the repository.
2. Install the dependencies:
    ```sh
    pipenv install
    ```
3. Create and activate a virtual environment:
    ```sh
    pipenv shell
    ```
4. Set up the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    python server/seed.py
    ```
5. Run the application:
    ```sh
    flask run
    ```

## Testing

Import the provided Postman collection (`challenge-2-superheroes.postman_collection.json`) into Postman to test the endpoints.

## License

This project is licensed under Claire Wambani.
