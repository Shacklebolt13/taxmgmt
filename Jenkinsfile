pipeline {
  agent none
  stages {
    stage('Environ Setup') {
      agent any
      steps {
        sh 'wget https://bootstrap.pypa.io/get-pip.py'
        sh 'python3 ./get-pip.py'
      }
    }
    stage('Build') {
      agent any
      steps {
        sh 'python3 -m pip install -r requirements.txt'
      }
    }
  }
}
