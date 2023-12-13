pipeline {
    agent {
        docker { image 'node:20.10.0-alpine3.19' }
    }
    options {
        skipStagesAfterUnstable()
    }
    stages {
         stage('Clone repository') { 
            steps { 
                script{
                checkout scm
                }
            }
        }
        stage('Build') { 
            steps { 
                script{
                    echo 'Build'
                    app = docker.build("pvrvl/pvrvl-mini-accounts-core-apis")
                }
            }
        }
        stage('Test'){
            steps {
                echo 'Empty'
            }
        }
        stage('Push Image') {
            steps {
                script{
                        docker.withRegistry('https://registry.hub.docker.com', 'docker-pvrvl') {
                            app.push("${env.BUILD_NUMBER}")
                            app.push("latest")
                        }
                }
            }
        }
    }
}
