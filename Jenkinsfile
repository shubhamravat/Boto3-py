pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                // Checkout the code from Git
                git 'https://github.com/shubhamravat/Boto3-py.git'
                
                // Run the Python script
                sh 'python insufficient.py' // Replace 'script_name.py' with the actual name of your Python script
            }
        }
    }
}
