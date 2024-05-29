pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                // Checkout the code from Git
                
                // Use Jenkins credentials to fetch AWS access key ID and secret access key
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'jenkins-user', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    sh "echo this is ${env.AWS_ACCESS_KEY_ID}"
                    sh "echo this is ${env.AWS_SECRET_ACCESS_KEY}"
                    // Run the Python script
                    echo 'running py script'               
                    script {
                        def uploadOutput = sh(returnStdout: true, script: 'sudo python3 insufficient.py')
                        echo "Python script output: ${uploadOutput}"
                    }
                }
            }
        }
    }
}
