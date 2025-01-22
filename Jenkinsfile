pipeline {
    agent any // Run on any available agent

    environment {
        BACKEND_USER = 'ubuntu'
        BACKEND_SERVER = '10.0.3.92'
        CHATAPP_DIR = '/Django_Chatapp'
        APP_USER = 'ubuntu'
        SERVICE_NAME = 'django-backend'
        SSH_KEY = '/var/lib/jenkins/.ssh/id_rsa' // Ensure this path is correct
    }

    stages {
        stage('Sync Files') {
            steps {
                script {
                    echo ">>> Starting file synchronization..."
                    try {
                        sh "rsync -avz -e 'ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no' ${WORKSPACE}/ ${BACKEND_USER}@${BACKEND_SERVER}:${CHATAPP_DIR}"
                    } catch (Exception e) {
                        echo "ERROR: File sync failed. Please check the SSH connection and directory permissions."
                        sh "exit 1"
                    }
                }
            }
        }

        stage('Execute Remote Tasks') {
            steps {
                script {
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
                    EOF
                    """
                }
            }
        }

        stage('Database Migrations') {
            steps {
                script {
                    sh """
                    ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${BACKEND_USER}@${BACKEND_SERVER} << 'EOF'
                    set -e

                    echo ">>> Navigating to the application directory..."
                    cd ${CHATAPP_DIR}

                    echo ">>> Running database migrations..."
                    python manage.py migrate
                    EOF
                    """
                }
            }
        }

        stage('Restart Application') {
            steps {
                script {
                    sh """
                    ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${BACKEND_USER}@${BACKEND_SERVER} << 'EOF'
                    set -e

                    echo ">>> Restarting the ${SERVICE_NAME} service..."
                    sudo systemctl restart ${SERVICE_NAME}

                    echo ">>> Deployment tasks completed for ${BACKEND_USER}!"
                    EOF
                    """
                }
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
