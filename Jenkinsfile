pipeline {
    agent any
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
                    app = docker.build("pvrvl-mini-accounts-core-apis")
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
                        docker.withRegistry('https://registry.hub.docker.com', "docker-pvrvl") {
                            app.push("${env.BUILD_NUMBER}")
                            app.push("latest")
                        }
                        echo 'Push Image'
                }
            }
        }
    }
}
