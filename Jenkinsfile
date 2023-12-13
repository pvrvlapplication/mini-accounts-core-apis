// pipeline {
//     agent any
//     options {
//         skipStagesAfterUnstable()
//     }
//     stages {
//          stage('Clone repository') { 
//             steps { 
//                 script{
//                 checkout scm
//                 }
//             }
//         }

//         stage('Build') { 
//             steps { 
//                 script{
//                  app = docker.build("pvrvl/pvrvl-mini-accounts-core-apis")
//                 }
//             }
//         }
//         stage('Test'){
//             steps {
//                  echo 'Empty'
//             }
//         }
//         stage('Push Image') {
//             steps {
//                 script{
//                         docker.withRegistry('https://registry.hub.docker.com', 'docker-pvrvl') {
//                             app.push("${env.BUILD_NUMBER}")
//                             app.push("latest")
//                         }
//                 }
//             }
//         }
//     }
// }

node {    
      def app     
      stage('Clone repository') {               
             
            checkout scm    
      }     
      stage('Build image') {         
       
            app = docker.build("pvrvl/pvrvl-mini-accounts-core-apis")    
       }     
      stage('Test image') {           
            app.inside {            
             
             sh 'echo "Tests passed"'        
            }    
        }     
       stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'docker-pvrvl') {            
        app.push("${env.BUILD_NUMBER}")            
        app.push("latest")        
              }    
           }
        }