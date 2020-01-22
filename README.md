# HRDC Database

This is my project to create an alternative to CaseWorthy. I'm going to use Python Flask to build the forms and interface logic, and SQLAlchemy to build the database logic.

## Current Version: 0.2

The current 'stable' version has a few core features:

- Clients
  - Create and update
  - Search
  - Add contact information
  - Add relationships between clients
- Services
  - Create programs and service types
  - Add services to a client
- Users
  - Manage user logins and password hashing


## Version 0.5 Goals

- Clients
  - All CRUD operations
- Services
  - All CRUD operations
  - Limit service types by program
    - e.g. only the warming center has the service type "emergency shelter"
- Users
  - Manage user roles (i.e. admin/regular)


## Version 1.0 Goals

- Generate CSBG All Characteristics report
  - Collect all relavent information about clients
- Generate other reports, similar to current CaseWorthy capabilities 