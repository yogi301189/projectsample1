pipeline {
  agent any
  environment {
    IMAGE = "yogi3011/projectsample"
    CRED = "dockerhub-creds"
  }
  stages {
    stage('Checkout') {
      steps { git 'https://github.com/yogi301189/projectsample1.git' }
    }
    stage('Build & Push') {
      steps {
        script {
          def commit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          docker.withRegistry('', CRED) {
            def img = docker.build("${IMAGE}:${commit}")
            img.push()
            img.push('latest')
          }
        }
      }
    }
  }
}
