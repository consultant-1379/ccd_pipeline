pipeline {
  agent {
    node {
      label 'ccd_pipeline_jenkins_agent'
    }
  }
  // The options directive is for configuration that applies to the whole job.
  options {
    buildDiscarder(logRotator(numToKeepStr:'30'))
    timeout(time: 240, unit: 'MINUTES')
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

    stage('Run Image Check on XDN SFTP') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          sh "cd ccd_pipeline/ansible; ansible-playbook -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} check-and-upload-images-to-xdn.yml -vvv" 
        }
      }
    }

    stage('Run Generate Config for deployment') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          sh "cd ccd_pipeline/ansible; ansible-playbook -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} generate-and-upload-conf-for-xdn.yml -vvv"
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
