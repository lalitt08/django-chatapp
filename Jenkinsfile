pipeline {
    agent any

    environment {
        SSH_KEY = '/var/lib/jenkins/.ssh/id_rsa'
        REMOTE_USER = 'ubuntu'
        REMOTE_HOST = '10.0.3.92'
        REMOTE_APP_DIR = '/Django_Chatapp'
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
                sh """
                    rsync -avz \$(pwd)/ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_APP_DIR}
                """
            }
        }

        stage('Setup and Run Backend Server') {
            steps {
                echo '>>> Setting up and running the backend server...'
                sh """
                    ssh -i ${SSH_KEY} ${REMOTE_USER}@${REMOTE_HOST} << 'EOF'
                    set -e
                    echo '>>> Sourcing environment variables from .bashrc...'
                    source ~/.bashrc

                    echo '>>> Activating virtual environment...'
                    source ${REMOTE_APP_DIR}/venv/bin/activate

                    echo '>>> Navigating to the application directory...'
                    cd ${REMOTE_APP_DIR}/fundoo

                    echo '>>> Installing dependencies from requirements.txt...'
                    pip install -r ${REMOTE_APP_DIR}/requirements.txt

                    echo '>>> Running database migrations...'
                    python manage.py migrate

                    echo '>>> Restarting the application service...'
                    sudo systemctl restart django-backend

                    echo '>>> Backend setup and service restart completed!'
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') { // Replace with your SonarQube server name
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=chatapp \
                        -Dsonar.sources=. \
                        -Dsonar.exclusions=**/venv/**,**/__pycache__/**,**/*.pyc,**/migrations/** \
                        -Dsonar.host.url=http://18.220.1.164:9000 \
                        -Dsonar.login=sqp_8b69d57f97cd25ef19a598d0638412eba36a5954 \
                        -Dsonar.sourceEncoding=UTF-8 \
                        -Dsonar.scm.exclusions.disabled=true \
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo '>>> Checking SonarQube Quality Gate...'
                script {
                    def qualityGate = waitForQualityGate()
                    if (qualityGate.status != 'OK') {
                        echo "WARNING: SonarQube Quality Gate failed with status: ${qualityGate.status}"
                        echo "Pipeline will continue despite Quality Gate failure."
                    } else {
                        echo "SonarQube Quality Gate passed with status: ${qualityGate.status}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo '>>> Deployment process finished!'
        }
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Deployment failed. Please check the logs for more details.'
        }
    }
}
