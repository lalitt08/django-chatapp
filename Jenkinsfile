pipeline {
    agent any

    environment {
        SSH_KEY = '/var/lib/jenkins/.ssh/id_rsa'
        REMOTE_USER = 'ubuntu'
        REMOTE_HOST = '10.0.3.92'
        REMOTE_APP_DIR = '/Django_Chatapp'
        SONAR_SCANNER_HOME = tool 'SonarScanner' // Use the name configured in Global Tool Configuration
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

        stage('SonarQube Analysis') {
            steps {
                echo '>>> Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube') { // Use the name configured in SonarQube Servers
                    sh """
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=chatapp-jenkins \
                        -Dsonar.sources=fundoo \
                        -Dsonar.host.url=http://18.220.1.164:9000 \
                        -Dsonar.login=sqp_0bdde7e8aef2d0da84f1c0c19533d3634b418ff9
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
                        error "Pipeline aborted due to SonarQube quality gate failure: ${qualityGate.status}"
                    }
                }
            }
        }

        stage('Execute Remote Tasks') {
            steps {
                echo '>>> Executing tasks on the backend server...'
                sh """
                    ssh -i ${SSH_KEY} ${REMOTE_USER}@${REMOTE_HOST} << 'EOF'
                    set -e
                    echo '>>> Sourcing environment variables from .bash_profile...'
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

                    echo '>>> Deployment tasks completed successfully!'
                """
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
