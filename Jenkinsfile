pipeline {
  agent any

  environment {
    IMAGE = "yogi3011/projectsample"      // DockerHub repo
    DOCKER_CRED = "dockerhub-creds"       // DockerHub credential ID
    SSH_CRED = "ec2-ssh"                   // SSH credential ID (the one that worked)
    EC2_USER = "ubuntu"                   // SSH username
    EC2_HOST = "13.204.69.38"             // EC2 public IP
    CONTAINER_NAME = "projectsample"      // container name on EC2
    APP_PORT = 5000                       // port Flask app uses inside container
    HOST_PORT = 5000                      // port exposed on EC2
  }

  stages {

    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Pre-check workspace') {
      steps {
        sh 'echo "Workspace files:"; ls -la || true'
        script {
          if (!fileExists('Dockerfile')) {
            error("Dockerfile missing in repo root.")
          }
        }
      }
    }

    stage('Get Commit') {
      steps {
        script {
          def commit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          env.SHORT_COMMIT = commit
          echo "Commit: ${commit}"
        }
      }
    }

    stage('Build & Push') {
      steps {
        script {
          def commit = env.SHORT_COMMIT
          docker.withRegistry('', "${DOCKER_CRED}") {
            def img = docker.build("${IMAGE}:${commit}")
            img.push()
            img.push('latest')
          }
        }
      }
    }

    stage('Deploy to EC2') {
      steps {
        script {
          def imageToDeploy = "${IMAGE}:${env.SHORT_COMMIT}"

          sshagent (credentials: ["${SSH_CRED}"]) {
            sh """
            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
            sudo docker pull ${imageToDeploy} &&
            sudo docker stop ${CONTAINER_NAME} || true &&
            sudo docker rm ${CONTAINER_NAME} || true &&
            sudo docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${APP_PORT} --restart unless-stopped ${imageToDeploy}
                '
            """

            sh """
               echo 'Waiting for app to start...' && sleep 5
               ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'docker ps | grep ${CONTAINER_NAME}'
            """
          }
        }
      }
    }

    stage('Post-deploy Health Check') {
      steps {
        script {
          def ok = false
          for (int i = 0; i < 6; i++) {
            def code = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://${EC2_HOST}:${HOST_PORT} || true", returnStdout: true).trim()
            echo "Health check attempt ${i + 1}, response: ${code}"
            if (code == '200' || code == '301' || code == '302') {
              ok = true
              break
            }
            sleep 5
          }
          if (!ok) error("App not responding on http://${EC2_HOST}:${HOST_PORT}")
        }
      }
    }
  }

  post {
    success { echo "Deployment successful: ${IMAGE}:${SHORT_COMMIT}" }
    failure { echo "Pipeline failed. Check logs." }
  }
}
