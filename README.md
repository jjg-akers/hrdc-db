# HRDC Database

This is my project to create an alternative to CaseWorthy. I'm going to use Python Flask to build the forms and interface logic, and SQLAlchemy to build the database logic.

## Current To-Dos:

- CreateClient form
  - Multiple values for race
  - Form validation
    - Duplicate Check
    - SSN formatting
      - ~~Check against existing entries~~
      - ~~Check for correct formatting~~
      - Allow partial ssns
    - Extra form field descriptions
  - Formatting
    - ~~Build generic form rendering template~~
- Client search functionality
- Build forms for other tables
  - Relationship
  - ClientContact
  - ClientAddress


## Future To-Dos:

- Implement other families of tables
  - Assessment
  - Service
- Make forms to create records in those tables
- Incorporate 'Current Client' information
  - Dashboard
- Reporting
  - Integrate pandas/seaborn
- Migrate data from CaseWorthy

## Future Future To-Dos:


- Testing
- Improve data security
- Research best ways to launch
  - AWS/GCP
  - Self-Host
- Automatic form filler
  - ServicePoint is a potential pilot
- Testing