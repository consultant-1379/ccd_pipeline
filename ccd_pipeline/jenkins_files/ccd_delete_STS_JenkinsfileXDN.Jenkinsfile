pipeline {
  agent {
    node {
      label 'ccd_pipeline_jenkins_agent'
    }
  }
  // The options directive is for configuration that applies to the whole job.
  options {
    buildDiscarder(logRotator(numToKeepStr:'30'))
    timeout(time: 90, unit: 'MINUTES')
    timestamps()
  }
  stages {

    stage('Set build name') {
      steps {
          script {
               currentBuild.displayName = "${env.BUILD_NUMBER} ${params.deployment_id}"
          }
      }
    }

    stage('Delete CCD') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          sh "cd ccd_pipeline/ansible; ansible-playbook -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} delete-ccd-stack-xdn.yml -vvv"
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
