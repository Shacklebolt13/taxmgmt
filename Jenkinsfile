pipeline {
  agent none
  stages {
    stage('Environ Setup') {
      agent any
      steps {
        sh 'wget https://bootstrap.pypa.io/get-pip.py'
        sh 'python3 ./get-pip.py'
        sh 'python3 -m pip install virtualenv'
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
