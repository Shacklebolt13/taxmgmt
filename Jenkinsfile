pipeline {
  agent none
  stages {
    stage('Environ Setup') {
      agent any
      steps {
        sh 'pip3 install virtualenv'
        sh 'python3 -m venv venv'
        sh 'source ./venv/bin/activate'
      }
    }
    stage('Build') {
      agent any
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
  }
}
