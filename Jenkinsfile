pipeline {
    agent any

    environment {
        DOCKER_IMAGE_APP = "my-python-app"
        DOCKER_IMAGE_TEST = "my-python-test"
        DOCKER_COMPOSE_FILE = "./Docker/docker-compose.yml"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'pipeline-test', url: 'https://github.com/Celer0n/panda-test.git'
            }
        }
        stage('Build Docker Image app') {
            steps {
                script {
                    def buildStatus = sh(script: "docker build -t ${DOCKER_IMAGE_APP} -f ./Docker/Dockerfile.app .", returnStatus: true)
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
                    def buildStatus = sh(script: "docker build -t ${DOCKER_IMAGE_TEST} -f ./Docker/Dockerfile.test .", returnStatus: true)
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
                        sh(
                            script: """
                            docker exec \$(docker ps -q -f ancestor=${DOCKER_IMAGE_TEST}) sh -c 'pip install requests pytest && pytest test_app.py'
                            """,
                            returnStatus: true
                        )
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