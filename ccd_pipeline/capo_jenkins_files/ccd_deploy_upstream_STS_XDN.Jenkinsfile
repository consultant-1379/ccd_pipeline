pipeline {
  agent {
    node {
      label 'capo_pipeline_jenkins_agent'
    }
  }
  // The options directive is for configuration that applies to the whole job.
  options {
    buildDiscarder(logRotator(numToKeepStr:'30'))
    timeout(time: 240, unit: 'MINUTES')
    timestamps()
  }
  
  environment {
    VAULT_FILE = credentials('ccd_pipeline_secret')
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
          sh "cd ccd_pipeline/capo_ansible; ansible-playbook -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} --vault-password-file $VAULT_FILE check-and-upload-images-to-xdn.yml -vvv" 
        }
      }
    }

    stage('Run Generate Config for deployment') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          sh "cd ccd_pipeline/capo_ansible; ansible-playbook -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} --vault-password-file $VAULT_FILE generate-and-upload-conf-for-xdn.yml -vvv"
        }
      }
    }

    // stage('Deploy CCD') {
    //   steps {
    //     withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
    //       sh "cd ccd_pipeline/capo_ansible; ansible-playbook -e deployment_id=${deployment_id}  -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} deploy-ccd-stack-xdn.yml -vvv"
    //     }
    //   }
    // }

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
