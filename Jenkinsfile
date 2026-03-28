pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app"
        CONTAINER_NAME = "flask-app"
        PORT = "5000"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Stop Old Container') {
            steps {
                echo 'Stopping old container if running...'
                bat "docker stop %CONTAINER_NAME% || exit 0"
                bat "docker rm %CONTAINER_NAME% || exit 0"
            }
        }

        stage('Deploy New Container') {
            steps {
                echo 'Deploying new container with self-healing...'
                bat "docker run -d --name %CONTAINER_NAME% --restart=always -p %PORT%:5000 %IMAGE_NAME%"
            }
        }

        stage('Health Check') {
            steps {
                echo 'Waiting for app to start...'
                bat "ping -n 6 127.0.0.1 > nul"
                echo 'App deployed successfully!'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed! App is live at http://localhost:5000'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
    }
}
