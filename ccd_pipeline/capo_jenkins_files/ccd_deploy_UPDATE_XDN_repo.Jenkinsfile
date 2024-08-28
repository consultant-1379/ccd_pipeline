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
  environment{
    SFTP_HOST = "sftp.sero.ict.ericsson.net" 
  }
  stages {
    stage('Set build name') {
      steps {
          script {
               currentBuild.displayName = "${env.BUILD_NUMBER}"
          }
      }
    }

    stage('Tar and push to sftp') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          tarAndUploadToSftp("${SFTP_USER}", "${SFTP_PASSWORD}", "${SFTP_HOST}", ".")
        }
      }
    }
  }
   post {
    success {
      echo 'Pipeline Successfully Completed'
    }
    failure {
      echo 'Pipeline Failed'
    }
  }
}


def tarAndUploadToSftp(String user,String password,String host,String dir ){
  sh"""
  tar cvf capo_repo.tgz ./*
  lftp -u $user,$password -e 'set sftp:connect-program "ssh -o StrictHostKeyChecking=no";put capo_repo.tgz -o ccd_pipeline/repo/capo_repo.tgz;exit' sftp://$host
  """
}