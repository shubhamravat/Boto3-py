pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                // Checkout the code from Git
                git 'https://github.com/shubhamravat/Boto3-py.git'
                echo 'git command ran'
                // Run the Python script
                echo 'running py script'
                sh 'python insufficient.py' // Replace 'script_name.py' with the actual name of your Python script
            }
        }
    }
}
