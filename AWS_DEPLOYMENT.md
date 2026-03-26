# AWS Elastic Beanstalk Deployment Guide

## Prerequisites

1. **AWS Account** - You already have this ✅
2. **AWS CLI** - Install it: https://aws.amazon.com/cli/
3. **EB CLI** - Install it: `pip install awsebcli`

## Step 1: Configure AWS Credentials

```bash
aws configure
```

You'll be prompted for:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format (press Enter for default)

Get your credentials from: **AWS Console** → **IAM** → **Users** → Your user → **Security credentials** → **Access keys**

## Step 2: Create MongoDB Atlas (Cloud Database)

Since AWS Elastic Beanstalk can't access local Docker containers, you need MongoDB in the cloud:

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account or sign in
3. Create a new project
4. Create a cluster (M0 tier is free)
5. Add your IP to whitelist (or use 0.0.0.0/0 for testing)
6. Create a database user (username/password)
7. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/ai_agent_db?retryWrites=true&w=majority`

## Step 3: Update `.env` File

Create `.env` file in project root with MongoDB Atlas URL:

```bash
USE_OPENAI=false
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/ai_agent_db?retryWrites=true&w=majority
```

**Important:** Add `.env` to `.gitignore` (already done) so secrets aren't exposed!

## Step 4: Initialize Elastic Beanstalk

```bash
cd C:\Users\peter\Desktop\AIAgent\ai-agent-mcp-server

# Initialize EB (in the same directory as your app)
eb init -p python-3.10 ai-study-helper --region us-east-1
```

This creates an `.elasticbeanstalk/config.yml` file.

## Step 5: Create and Deploy

```bash
# Create environment and deploy (first time)
eb create ai-study-helper-env

# This will:
# - Create an EC2 instance
# - Install dependencies from requirements.txt
# - Deploy your app
# - Give you a public URL

# Wait 5-10 minutes for deployment to complete
```

## Step 6: Set Environment Variables on AWS

```bash
# Set MONGO_URL on the server
eb setenv MONGO_URL="mongodb+srv://username:password@cluster.mongodb.net/ai_agent_db?retryWrites=true&w=majority"
eb setenv USE_OPENAI=false

# Restart the app
eb restart
```

## Step 7: Get Your Public URL

```bash
# Display environment URL
eb open
```

Or find it in AWS Console:
- **AWS Elastic Beanstalk** → **Environments** → **ai-study-helper-env** → **Domain**

Example: `http://ai-study-helper-env.us-east-1.elasticbeanstalk.com`

## Step 8: Share with Your Manager

Send your manager this URL:
```
http://ai-study-helper-env.us-east-1.elasticbeanstalk.com
```

They can now:
- ✅ Generate study materials
- ✅ View saved materials
- ✅ Search materials
- ✅ All from their browser, anywhere!

---

## Useful Commands

```bash
# View logs
eb logs

# Check status
eb status

# View environment variables
eb printenv

# SSH into instance
eb ssh

# Terminate environment (stop charges)
eb terminate ai-study-helper-env

# Deploy updates
git add .
git commit -m "Update app"
eb deploy
```

---

## Troubleshooting

### App not loading?
```bash
eb logs --stream
```

### Environment variable not set?
```bash
eb setenv VAR_NAME=value
eb restart
```

### MongoDB connection error?
1. Check connection string in `.env`
2. Verify whitelist in MongoDB Atlas
3. Check username/password

### Want to use your local MongoDB?
You'd need to:
1. Deploy MongoDB separately (AWS DocumentDB costs money)
2. Use MongoDB Atlas (easier, free tier available)

---

## Cost Considerations

**Free Tier:**
- ✅ EC2 (t2.micro) - **Free for 12 months**
- ✅ MongoDB Atlas - **Free tier available** (512MB storage)

**Estimated Monthly Cost:** $0-5 (if using free tiers)

---

## Next Steps

1. Set up MongoDB Atlas
2. Update `.env` with MongoDB Atlas URL
3. Run `eb init` and `eb create`
4. Share URL with manager
5. Done! 🚀

Need help? Check AWS Elastic Beanstalk docs: https://docs.aws.amazon.com/elasticbeanstalk/
