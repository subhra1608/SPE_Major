pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('subhra1608-dockerhub')
        GITHUB_REPO_URL = 'https://github.com/subhra1608/SPE_MAJOR.git'
        DOCKER_PORT = '7070' // Define the port to use for Docker services
        DOCKER_PORT_2 = '7090' // Define another port for Ansible playbook stage
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Checkout source code
                    checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/subhra1608/SPE_Major.git']])
                }
            }
        }
        
        stage('Install Python and Flask') {
            steps {
                // Update package index and install Python 3 and pip without sudo
                sh 'sudo apt update'
                sh 'sudo apt install -y python3 python3-pip'
                
                // Install Flask using pip
                sh 'sudo pip3 install Flask pandas flask_cors requests'
            }
        }
        
        stage('Run Integration Tests') {
            steps {
                script {
                    // Run integration tests
                    sh 'pip install -r requirements.txt'
                    sh 'nohup python3 app.py &'
                    sh 'python3 test_app.py'
                }
            }
        }
        
        
        stage('Build Docker Images') {
            steps {
                // Build frontend Docker image
                sh 'docker-compose -f docker-compose.yml build frontend'
                
                // Build backend Docker image
                sh 'docker-compose -f docker-compose.yml build backend'
            }
        }

        stage('Push Docker Images') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker-compose push'
            }
        }
        
        stage('Start Services Detached') {
            steps {
                script {
                    // Modify Docker Compose file dynamically to use port 7070
                    sh "sed -i 's/2060:2060/$DOCKER_PORT:2060/g' docker-compose.yml"
                    // Start Docker services in detached mode
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
        
        
        stage('Verify Ansible Installation') {
            steps {
                sh 'ansible --version'
            }
        }

         stage('Run Ansible Playbook') {
            steps {
                script {
                    // Modify Docker Compose file dynamically to use port 7070
                   sh "sed -i 's/2060:2060/$DOCKER_PORT:2060/g' docker-compose.yml"
                    
                    // Execute the modified playbook
                    ansiblePlaybook(
                        playbook: 'plybk_local.yml',
                        inventory: 'inventory'
                    )
                }
            }
        }


    }
}
