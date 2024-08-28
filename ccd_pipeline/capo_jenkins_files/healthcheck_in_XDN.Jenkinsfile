pipeline {
  agent {
    node {
      label 'capo_pipeline_jenkins_agent'
    }
  }
  environment {
    VAULT_FILE = credentials('ccd_pipeline_secret')
  }
  // The options directive is for configuration that applies to the whole job.
  options {
    buildDiscarder(logRotator(numToKeepStr:'30'))
    timeout(time: 40, unit: 'MINUTES')
    timestamps()
  }
  parameters {
        string(
            name: 'deployment_id',
            defaultValue: 'stsvpXccdXX',
            description: 'Name of CCD deployment.\nPlease read following http://wiki.stsoss.seli.gic.ericsson.se:8080//index.php/CAPO_pipeline_in_ECN',
            trim: true
        )
  }	
  stages {
    stage('Set build name') {
      steps {
          script {
               currentBuild.displayName = "${env.BUILD_NUMBER} ${params.deployment_id}"
          }
      }
    }
    stage('Run deployment Healthcheck') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          sh "cd ccd_pipeline/capo_ansible; ansible-playbook -vvv -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD}  --vault-password-file $VAULT_FILE healthcheck-in-xdn.yml"
        }
      }
    }
  }
  // The post build actions
  post {
    success {
      echo 'Pipeline Successfully Completed'
    }
    failure {
      echo 'Pipeline Failed'
    }
  }
}
