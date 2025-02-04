#!/bin/bash
# Navigate to the deployment-archive directory
cd /opt/codedeploy-agent/deployment-root/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/deployment-archive/

# Unzip the Django_Chatapp.zip into the desired target directory
unzip Django_Chatapp.zip -d /Django_Chatapp/
