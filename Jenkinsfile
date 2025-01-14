pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my-python-app"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Celer0n/panda-test.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }
        stage('Run Docker Compose') {
            steps {
                script {
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d"
                }
            }
        }
        stage('Test Application') {
            steps {
                script {
                    sh "pip install requests pytest"
                    sh "pytest test_app.py"
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} down"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
    }
}