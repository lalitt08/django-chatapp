pipeline {
    agent any
    environment {
        SSH_KEY = '/var/lib/jenkins/.ssh/id_rsa' // Specify the SSH private key
    }
    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                echo 'Checking out the repository...'
                checkout scm
            }
        }
        stage('Sync Files') {
            steps {
                echo '>>> Starting file synchronization...'
                sh '''
                    rsync -avz -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \
                    ${WORKSPACE}/ ubuntu@10.0.3.92:/Django_Chatapp
                '''
            }
        }
        stage('Execute Remote Tasks') {
            steps {
                echo '>>> Executing tasks on the backend server...'
                sh '''
                    ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ubuntu@10.0.3.92 << EOF
                    set -e  # Exit immediately if a command fails
                    echo '>>> Activating virtual environment...'
                    source /Django_Chatapp/venv/bin/activate

                    echo '>>> Navigating to the application directory...'
                    cd /Django_Chatapp/fundoo

                    echo '>>> Installing dependencies from requirements.txt...'
                    pip install -r /Django_Chatapp/requirements.txt

                    echo '>>> Running database migrations...'
                    python manage.py migrate

                    echo '>>> Restarting the application service...'
                    sudo systemctl restart django-backend

                    echo '>>> Deployment tasks completed successfully!'
                    EOF
                '''
            }
        }
    }
    post {
        success {
            echo '>>> Deployment process finished successfully!'
        }
        failure {
            echo 'Deployment failed. Please check the logs for more details.'
        }
    }
}
