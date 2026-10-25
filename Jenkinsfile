
pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    set -e
                    .venv/bin/python app.py > flask.log 2>&1 &
                    APP_PID=$!
                    trap 'kill $APP_PID 2>/dev/null || true' EXIT

                    for i in $(seq 1 30); do
                        if curl -fsS http://127.0.0.1:5002/ >/dev/null; then
                            break
                        fi
                        sleep 2
                    done

                    curl -fsS http://127.0.0.1:5002/ >/dev/null
                    .venv/bin/python -m pytest -v tests/test_registrationapp.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t nisha1310/week12-registration:v1 .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh '''
                        set +x
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" --password-stdin
                        docker push nisha1310/week12-registration:v1
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    kubectl rollout status deployment/seleniumtestdemoapp-deployment \
                        --timeout=120s
                '''
            }
        }
    }

    post {
        success {
            echo 'Week 12 pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
