pipeline {
  agent any

parameters {
  string(name: 'PYTEST_MARKER', defaultValue: 'TC6 or TC7', description: 'Pytest marker expression (e.g., TC6, TC6 or TC7, ui, api, regression)')
  booleanParam(name: 'RUN_TARGETED', defaultValue: true, description: 'Run targeted marker tests before full regression')
  booleanParam(name: 'RUN_REGRESSION', defaultValue: false, description: 'Run full regression suite')
  booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Run browser in headless mode')
  booleanParam(name: 'RECORD_VIDEO', defaultValue: false, description: 'Record test videos on failure')
  booleanParam(name: 'PARALLEL', defaultValue: true, description: 'Run tests in parallel')
  string(name: 'EXTRA_PYTEST_ARGS', defaultValue: '', description: 'Additional pytest arguments (e.g., --tb=short, -k "login")')
}

  environment {
    BASE_URL = 'https://automationexercise.com'
    PLAYWRIGHT_DEFAULT_TIMEOUT = '15000'
    AUTO_GENERATE_ALLURE = 'false'
    # Set from parameters
    HEADLESS = "${params.HEADLESS}"
    RECORD_VIDEO = "${params.RECORD_VIDEO}"
    # Optional: Configure in Jenkins credentials
    # LIST_OF_CREDENTIALS = credentials('test-credentials-json')
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
          set -e  # Fail on any error
          python3 --version
          python3 -m pip install --upgrade pip
          python3 -m pip install -r requirements.txt
        '''
      }
    }

    stage('Install Playwright Browsers') {
      steps {
        sh '''
          set -e  # Fail on any error
          python3 -m playwright install --with-deps || python3 -m playwright install
        '''
      }
    }

    stage('Agentic Init Verification') {
      steps {
        // Use unified init scripts from .kilo (canonical location)
        // Fallback to .cursor if .kilo not yet synced
        sh '''
          set -e  # Fail on any error
          if [ -f ".kilo/skills/init/scripts/verify_env.py" ]; then
            python3 .kilo/skills/init/scripts/verify_env.py
            python3 .kilo/skills/init/scripts/smoke_collect.py
          elif [ -f ".cursor/skills/init/scripts/verify_env.py" ]; then
            echo "[INFO] Using .cursor init scripts (legacy)"
            python3 .cursor/skills/init/scripts/verify_env.py
            python3 .cursor/skills/init/scripts/smoke_collect.py
          else
            echo "[ERROR] No init scripts found in .kilo or .cursor"
            exit 1
          fi
        '''
      }
    }

    stage('Test Collection Validation') {
      steps {
        sh '''
          set -e  # Fail on any error
          echo "Validating test discovery..."
          pytest --collect-only -q
        '''
      }
    }

    stage('Run Targeted Tests') {
      when {
        expression { return params.RUN_TARGETED }
      }
      steps {
        sh '''
          set -e  # Fail on any error
          echo "Running targeted tests with marker: ${PYTEST_MARKER}"
          echo "HEADLESS=${HEADLESS}, RECORD_VIDEO=${RECORD_VIDEO}, PARALLEL=${PARALLEL}"

          # Build pytest arguments as array for safe handling
          PYTEST_ARGS=(-m "${PYTEST_MARKER}")

          # Add parallel if enabled
          if [ "${PARALLEL}" = "true" ]; then
            PYTEST_ARGS+=(-n auto --dist loadscope)
          fi

          # Add extra args (split by whitespace)
          if [ -n "${EXTRA_PYTEST_ARGS}" ]; then
            # shellcheck disable=SC2206
            EXTRA_ARGGROUP=(${EXTRA_PYTEST_ARGS})
            PYTEST_ARGS+=("${EXTRA_ARGGROUP[@]}")
          fi

          # Run tests (addopts from pytest.ini will add HTML/Allure reporting automatically)
          pytest "${PYTEST_ARGS[@]}"
        '''
      }
    }

    stage('Run Full Regression') {
      when {
        expression { return params.RUN_REGRESSION }
      }
      steps {
        sh '''
          set -e  # Fail on any error
          echo "Running full regression suite..."

          PYTEST_ARGS=(-m regression)

          # Add parallel if enabled
          if [ "${PARALLEL}" = "true" ]; then
            PYTEST_ARGS+=(-n auto --dist loadscope)
          fi

          # Add extra args (split by whitespace)
          if [ -n "${EXTRA_PYTEST_ARGS}" ]; then
            # shellcheck disable=SC2206
            EXTRA_ARGGROUP=(${EXTRA_PYTEST_ARGS})
            PYTEST_ARGS+=("${EXTRA_ARGGROUP[@]}")
          fi

          pytest "${PYTEST_ARGS[@]}"
        '''
      }
    }

    stage('Generate Allure Report') {
      when {
        expression { return fileExists('allure-results') }
      }
      steps {
        sh '''
          if [ -d "allure-results" ] && [ "$(ls -A allure-results)" ]; then
            if command -v npx &> /dev/null; then
              npx allure generate allure-results -o allure-report --clean
            else
              echo "[WARN] npx not found. Skipping Allure HTML generation. Install Node.js to generate HTML reports."
              echo "[INFO] You can still view results with: npx allure serve allure-results"
            fi
          else
            echo "[INFO] No Allure results found"
          fi
        '''
      }
    }
  }

   post {
     always {
       // Archive test artifacts
       archiveArtifacts artifacts: 'test-results/**,allure-results/**,allure-report/**/*', allowEmptyArchive: true
       
       // Publish JUnit XML for Jenkins test reporting (if available)
       junit testResults: 'test-results/**/*.xml', allowEmptyResults: true
       
       // Publish HTML reports (if available)
       publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'test-results/reports', reportFiles: 'report.html', reportName: 'Pytest HTML Report'])
       publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'allure-report', reportFiles: 'index.html', reportName: 'Allure Report'])
     }
    
    success {
      echo '✅ Pipeline completed successfully'
      // Optional: Slack/email notification
    }
    
    failure {
      echo '❌ Pipeline failed. Check test-results/ and allure-results/ for details.'
      // Optional: slackSend channel: '#qa-automation', message: "Build ${env.BUILD_NUMBER} failed: ${env.JOB_NAME}"
    }
    
    unstable {
      echo '⚠️ Pipeline unstable (test failures or flaky tests detected)'
    }
  }
}
