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
    timeout(time: 150, unit: 'MINUTES')
    timestamps()
  }
  // Stages defined here
  stages {
    stage('list images /proj/ossststools') {
      steps {
        sh "ls /proj/ossststools/ECCD/IMAGES"
      }
    }
    stage('Set build name') {
      steps {
          script {
               currentBuild.displayName = "${env.BUILD_NUMBER} ${params.deployment_id}"
          }
      }
    }
    stage('Deploy CCD') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          sh "cd ccd_pipeline/capo_ansible; ansible-playbook -vvv -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} --vault-password-file $VAULT_FILE deploy-capo-cluster-in-xdn.yml"
        }
      }
    }
    stage('upload files to deployment minio') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          sh "cd ccd_pipeline/capo_ansible; ansible-playbook -vvv -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} --vault-password-file $VAULT_FILE upload-ccd-info-to-minio-in-xdn.yml"
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
      //echo 'Pipeline Exiting OQS Queue'
      //sh "cd capo_ansible; ansible-playbook -vvv -e deployment_id=${deployment_id} --vault-password-file $VAULT_FILE leave-oqs-queue.yml"
    }
  }
}
