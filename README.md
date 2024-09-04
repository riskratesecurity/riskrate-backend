# README.md

To start the development work, follow the instructions below:

1. Make sure you have Docker Compose installed on your machine.

2. Create a `.env` file in the root directory of the project with the following content:

    ```
    DATABASE_URL=postgresql://postgres:postgres@localhost:5432/riskrate_dev
    ```

3. Run the following command to start the development database:

    ```
    docker-compose up -d
    ```

4. To run the unit tests, use the following command:

    ```
    uv run pytest src/tests
    ```

Remember that all project management will be done through "uv".