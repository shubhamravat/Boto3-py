pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                // Checkout the code from Git
                
                // Upload the file to S3
                sh 'sudo python3 insufficient.py' // Replace this with your upload to S3 step if needed
                
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
