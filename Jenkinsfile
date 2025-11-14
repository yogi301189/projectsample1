pipeline {
  agent any

  environment {
    IMAGE = "yogi3011/projectsample"
    CRED  = "dockerhub-creds"
  }

  stages {
    stage('Declarative: Checkout SCM') {
      steps {
        // Use the same checkout Jenkins already did for the pipeline
        checkout scm
      }
    }

    stage('Get Commit') {
      steps {
        script {
          // get short SHA from the workspace
          COMMIT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          echo "Using commit: ${COMMIT}"
        }
      }
    }

    stage('Build & Push') {
      steps {
        script {
          docker.withRegistry('', CRED) {
            def img = docker.build("${IMAGE}:${COMMIT}")
            img.push()
            img.push('latest')
          }
        }
      }
    }
  }

  post {
    success { echo "Pushed ${IMAGE}:${COMMIT} and :latest" }
    failure { echo "Pipeline failed" }
  }
}
