// Jenkinsfile — Declarative Pipeline
// Replace YOUR_DOCKERHUB_USERNAME with your actual Docker Hub username

pipeline {

    // Run on any available Jenkins agent
    agent any

    // --- Pipeline-wide variables ---
    environment {
        IMAGE_NAME  = "goliakash/flask-k8s-app"
        IMAGE_TAG   = "${BUILD_NUMBER}"   // each build gets a unique tag (e.g. :42)
        // 'dockerhub-creds' is the ID of the credential you add in Jenkins > Manage Credentials
        DOCKER_CRED = credentials('dockerhub-creds')
    }

    stages {

        // 1. Pull the source code
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // 2. Install deps and run tests
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                    pytest tests/ -v
                '''
            }
        }

        // 3. Build the Docker image
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                // Also tag as 'latest' so K8s can pull the newest version easily
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }

        // 4. Push image to Docker Hub
        stage('Push to Registry') {
            steps {
                sh "echo ${DOCKER_CRED_PSW} | docker login -u ${DOCKER_CRED_USR} --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        // 5. Deploy to Kubernetes
        stage('Deploy to Kubernetes') {
            steps {
                // Update the image tag in the deployment manifest on the fly, then apply
                sh """
                    sed -i 's|IMAGE_PLACEHOLDER|${IMAGE_NAME}:${IMAGE_TAG}|g' k8s/deployment.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/flask-app --timeout=60s
                """
            }
        }
    }

    // --- Post-pipeline actions ---
    post {
        success {
            echo "Pipeline succeeded! App is live."
        }
        failure {
            echo "Pipeline failed. Check the logs above."
        }
    }
}