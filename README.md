# drone-ecs-deploy
A Drone plugin for deploying Amazon ECS services.

This plugin is built to suit only a specific workflow which meets some assumptions:

- The services and tasks definiton already exist in Amazon ECS (in my case they are created by a TerraForm IaC project apart from microservices projects).

- There is a task definition and a tag on Docker registry for each environment (ex.: stg, prd etc.). So deploy a new version of a microservice just means move that tag to a new Docker image version and force a service deployment without the need for any task updates.

## Usage

```
steps:
  - name: "Deploy to integration environment"
    image: diegoaltx/drone-ecs-deploy:1
    settings:
      cluster: application-integration
      service: microservice-example
    when:
      ref:
        - refs/heads/master

  - name: "Deploy to staging environment"
    image: diegoaltx/drone-ecs-deploy:1
    settings:
      cluster: application-staging
      service: microservice-example
    when:
      ref:
        - refs/tags/v*[0-9].*[0-9].*[0-9]*-rc*.*[0-9]

  - name: "Deploy to production environment"
    image: diegoaltx/drone-ecs-deploy:1
    settings:
      cluster: application-production
      service: microservice-example
    when:
      ref:
        - refs/tags/v*[0-9].*[0-9].*[0-9]*-stable
```

## Settings

| Key                              | Description           |
|----------------------------------|-----------------------|
| **cluster** *required*           | cluster name          |
| **service** *required*           | service name          |
| **access_key_id** *optional*     | AWS access key id     |
| **secret_access_key** *optional* | AWS secret access key |
| **region** *optional*            | AWS region            |
