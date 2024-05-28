pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                // Checkout the code from Git
                // Run the Python script
                echo 'running py script'               
                sh 'sudo python3 insufficient.py' // Replace 'script_name.py' with the actual name of your Python script
            }
        }
    }
}
