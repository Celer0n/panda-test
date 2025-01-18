pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my-python-app"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'development', url: 'https://github.com/Celer0n/panda-test.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def buildStatus = sh(script: "docker build -t ${DOCKER_IMAGE} .", returnStatus: true)
                    if (buildStatus != 0) {
                        echo "Docker image build failed with status: ${buildStatus}"
                        error("Stopping pipeline due to failure in building Docker image.")
                    }
                }
            }
        }
        stage('Run Docker Compose') {
            steps {
                script {
                    def composeStatus = sh(script: "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d", returnStatus: true)
                    if (composeStatus != 0) {
                        echo "Docker Compose failed with status: ${composeStatus}"
                        error("Stopping pipeline due to failure in Docker Compose.")
                    }
                }
            }
        }
        stage('Test Application') {
            steps {
                script {
                    try {
                        // Run tests inside the Docker container
                        sh """
                        docker exec $(docker ps -q -f ancestor=${DOCKER_IMAGE}) sh -c "
                            pip install requests pytest && 
                            pytest test_app.py"
                        """
                    } catch (Exception e) {
                        echo "Test stage failed: ${e}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    try {
                        sh "docker-compose -f ${DOCKER_COMPOSE_FILE} down"
                    } catch (Exception e) {
                        echo "Cleanup stage encountered an error: ${e}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}