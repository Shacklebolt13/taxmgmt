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
        sh 'rm -f db.sqlite3 '
        sh 'python3 manage.py migrate'        
        sh 'python3 manage.py makeadmin'
      }
    }
    
    stage('Db Init') {
      agent any
      steps {
        sh 'python3 manage.py initDb'
      }
    }
    
    stage('Test') {
      agent any
      steps {
        sh 'python3 manage.py test'
      }
    }
  }
}
