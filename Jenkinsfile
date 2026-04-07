pipeline {
  agent any

  parameters {
    string(name: 'PYTEST_MARKER', defaultValue: 'TC6 or TC7', description: 'Pytest marker expression')
    booleanParam(name: 'RUN_TARGETED', defaultValue: true, description: 'Run targeted marker tests')
  }

  environment {
    BASE_URL = 'https://automationexercise.com'
    RECORD_VIDEO = 'false'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python') {
      steps {
        sh '''
          python3 --version
          python3 -m pip install --upgrade pip
          python3 -m pip install -r requirements.txt
        '''
      }
    }

    stage('Install Playwright Browsers') {
      steps {
        sh '''
          python3 -m playwright install --with-deps || python3 -m playwright install
        '''
      }
    }

    stage('Agentic Init Verification') {
      steps {
        sh '''
          python3 .cursor/skills/init/scripts/verify_env.py
          python3 .cursor/skills/init/scripts/smoke_collect.py
        '''
      }
    }

    stage('Run Targeted Tests') {
      when {
        expression { return params.RUN_TARGETED }
      }
      steps {
        sh '''
          pytest -m "${PYTEST_MARKER}" -q
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'test-results/**,allure-results/**', allowEmptyArchive: true
      junit testResults: 'test-results/**/*.xml', allowEmptyResults: true
    }
  }
}
