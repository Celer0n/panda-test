pipeline {
    agent any

    environment {
        DOCKER_IMAGE_APP = "my-python-app"
        DOCKER_IMAGE_TEST = "my-python-test"
        DOCKER_COMPOSE_FILE = "./Docker/docker-compose.yml"
        IMAGE_VERSION = "v1.0.3"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'test', url: 'https://github.com/Celer0n/panda-test.git'
            }
        }

        stage('Build Docker Image app') {
            steps {
                script {
                    def buildStatus = sh(script: """
                        docker build -t ${DOCKER_IMAGE_APP}:${IMAGE_VERSION} -f ./Docker/Dockerfile.app .
                        docker tag ${DOCKER_IMAGE_APP}:${IMAGE_VERSION} ${DOCKER_IMAGE_APP}:latest
                    """, returnStatus: true)
                    if (buildStatus != 0) {
                        echo "Docker image build failed with status: ${buildStatus}"
                        error("Stopping pipeline due to failure in building Docker image.")
                    }
                }
            }
        }

        stage('Build Docker Image test') {
            steps {
                script {
                    def buildStatus = sh(script: """
                        docker build -t ${DOCKER_IMAGE_TEST}:${IMAGE_VERSION} -f ./Docker/Dockerfile.test .
                        docker tag ${DOCKER_IMAGE_TEST}:${IMAGE_VERSION} ${DOCKER_IMAGE_TEST}:latest
                    """, returnStatus: true)
                    if (buildStatus != 0) {
                        echo "Docker image build failed with status: ${buildStatus}"
                        error("Stopping pipeline due to failure in building Docker image.")
                    }
                }
            }
        }

        stage('Run Docker Compose for Tests') {
            steps {
                script {
                    def composeStatus = sh(script: """
                        docker-compose -f ${DOCKER_COMPOSE_FILE} up -d
                    """, returnStatus: true)
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
                        sh """
                        docker exec \$(docker ps -q -f ancestor=${DOCKER_IMAGE_TEST}) sh -c 'pip install requests pytest && pytest test_app.py'
                        """
                    } catch (Exception e) {
                        echo "Test stage failed: ${e}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }

        stage('Stop Test Containers') {
            steps {
                script {
                    echo "Stopping test containers..."
                    sh """
                    docker-compose -f ${DOCKER_COMPOSE_FILE} stop testweb
                    docker-compose -f ${DOCKER_COMPOSE_FILE} rm -f testweb
                    """
                }
            }
        }

        stage('Run App Container Only') {
            steps {
                script {
                    echo "Starting only the application container..."
                    sh """
                    docker-compose -f ${DOCKER_COMPOSE_FILE} up -d web
                    """
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