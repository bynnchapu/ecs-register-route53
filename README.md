ecs-register-route53
====================

This image get PublicIP of the ECS task and update the IP address
to specified DNS record on the rotue53.

Environment Variables
---------------------

This Docker image uses following environment variables by `register-route53.py` script.

- `REGION`: Specify AWS region for running ECS cluster and service
- `CLUSTER`: Specify cluster name for ECS
- `SERVICE`: Specify service name in the `CLUSTER` for ECS
- `HOSTED_ZONE`: Specify hosted zone for Route53
- `RECORD_NAME`: Specify Record name in the `HOSTED_ZONE` for ECS
- `DEBUG`: If it is spefified `TRUE`, show debug message