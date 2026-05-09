# Cloud counter

A simple Azure web application that counts how many times the page was loaded, developed as an assignment for a university course.

## CI/CD pipeline

The project is packaged, built, and deployed automatically on push in 3 stages. The `package` phase adds a commit hash to the page template and randomizes the heading color. Afterward, the `build` phase verifies that the application can be run. And the last stage, `deploy`, deploys static files and application code.

## Persistence

The counter number is stored in Table Storage. The static files (CSS) are in Blob Storage and accessed via custom `/static` redirects.

## Secretless configuration

There are no connection strings in the application. Entra ID Managed Identity is used instead.
