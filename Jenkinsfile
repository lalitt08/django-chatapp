pipeline {
    agent any
    environment {
        BACKEND_USER = 'ubuntu'
        BACKEND_SERVER = '10.0.3.92'
        CHATAPP_DIR = '/Django_Chatapp/fundoo' // Updated to include the 'fundoo' subdirectory
        SSH_KEY = '/var/lib/jenkins/.ssh/id_rsa'
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
                sh """
                ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${BACKEND_USER}@${BACKEND_SERVER} << 'EOF'
                set -e

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
