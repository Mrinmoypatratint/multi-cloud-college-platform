# Multi-Cloud Deployment & Operations Manual

## Cloud Strategy Overview
This platform employs a resilient **Multi-Cloud Architecture**:
- **AWS (Primary Production)**: Hosts active production traffic across AWS ECS Fargate, AWS RDS PostgreSQL Multi-AZ, and ALB.
- **Azure (Staging & Failover DR)**: Serves as staging environment and warm-standby Disaster Recovery site.

---

## 🌩️ 1. AWS Production Setup

### Terraform Provisioning
```bash
cd infrastructure/aws
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

### AWS Deployment Steps
1. Push Docker images to **AWS ECR**:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
   docker tag college-backend:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/college-backend:latest
   docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/college-backend:latest
   ```
2. Force ECS deployment update:
   ```bash
   aws ecs update-service --cluster educloud-prod-cluster --service educloud-backend-service --force-new-deployment
   ```

---

## 🟦 2. Azure Staging / Failover Setup

### Terraform Provisioning
```bash
cd infrastructure/azure
terraform init
terraform apply -auto-approve
```

---

## 🔄 Rollback & Disaster Recovery Strategy

- **Automated Failover**: Azure Front Door / Route 53 health check switches traffic automatically if AWS ALB fails health probe.
- **Database Backup**: Multi-AZ RDS automated daily snapshots retained for 35 days with Point-In-Time Restore capability.
