pipeline {
    agent any
    environment {
        REPO_URL = 'git@github.com:opti93/api-flask.git'
        USER = 'deployer'
        SERVER_IP = '54.93.57.80'
        SERVER_URL = '54.93.57.80:8888'
    }
    stages {
        // Pulling repository with application
        stage('Checkout') {
            steps {
                echo "Pulling api-flask code from GitHub"
                checkout([$class: 'GitSCM', 
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: REPO_URL,
                        credentialsId: 'github'
                    ]]
                ])
            }
        }
        // Buuiding docker image
        stage('Build') {
            steps {
                echo "Build docker image"
                sh "docker build -t api-flask ."
                sh "docker tag api-flask:latest 139701481425.dkr.ecr.eu-central-1.amazonaws.com/api-flask:$BUILD_NUMBER"
            }
        }
        // Pushing docker image to ECR repository
        stage('Push') {
            steps {
                echo "Pushing docker image to ECR"
                sh "aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 139701481425.dkr.ecr.eu-central-1.amazonaws.com"
                sh "docker push 139701481425.dkr.ecr.eu-central-1.amazonaws.com/api-flask:$BUILD_NUMBER"
            }
        }
        // Deploing application on server by docker compose
        stage('CD-part') {
            steps {
                echo "Deploing application"
                sshagent(['deployer']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no $USER@$SERVER_IP "aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 139701481425.dkr.ecr.eu-central-1.amazonaws.com && export IMAGE_NAME=139701481425.dkr.ecr.eu-central-1.amazonaws.com/api-flask && export IMAGE_TAG=$BUILD_NUMBER  && docker compose -f /opt/app/docker-compose.yml up -d --force-recreate"
                    """
                }
            }
        }
        // Testing application if 200 http code returned then OK else job fails
        stage('Testing accessibility of application') {
            steps {
                script {
                    // Perform the curl request and check the HTTP status code
                    def response = sh(script: "curl -o /dev/null -s -w '%{http_code}' $SERVER_URL", returnStdout: true).trim()
                    
                    // Check if the response code is 200
                    if (response != '200') {
                        error "Application returned HTTP status code $response. Failing pipeline."
                    } else {
                        echo "Application is healthy. HTTP status code: 200."
                    }
                }
            }
        }
    }
}