pipeline {
    agent any // This specifies that the pipeline can run on any available agent
    environment {
        // Define the environment variables
        BACKEND_USER = 'ubuntu'
        BACKEND_SERVER = '10.0.3.92'
        CHATAPP_DIR = '/Django_Chatapp'
        SSH_KEY = '/var/lib/jenkins/.ssh/id_rsa' // Ensure this is the correct path to your SSH private key
    }
    stages {
        stage('Sync Files') {
            steps {
                echo ">>> Starting file synchronization..."
                sh "rsync -avz -e 'ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no' ${WORKSPACE}/ ${BACKEND_USER}@${BACKEND_SERVER}:${CHATAPP_DIR}"
            }
        }
        stage('Execute Remote Tasks') {
            steps {
                echo ">>> Executing tasks on the backend server..."
                // Using a script step to execute multiple commands via SSH
                sh """
                ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${BACKEND_USER}@${BACKEND_SERVER} << 'EOF'
                set -e  # Ensure the shell exits immediately if any command exits with a non-zero status

                echo ">>> Activating virtual environment..."
                source ${CHATAPP_DIR}/venv/bin/activate

                echo ">>> Navigating to the application directory..."
                cd ${CHATAPP_DIR}

                echo ">>> Installing dependencies from requirements.txt..."
                pip install -r requirements.txt

                echo ">>> Running database migrations..."
                python manage.py migrate

                echo ">>> Restarting the application service..."
                sudo systemctl restart django-backend

                echo ">>> Deployment tasks completed!"
                EOF
                """
            }
        }
    }
    post {
        always {
            echo '>>> Deployment process finished!'
        }
        success {
            echo 'Deployment completed successfully.'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
