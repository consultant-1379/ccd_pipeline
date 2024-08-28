pipeline {
  agent {
    node {
      label 'capo_pipeline_jenkins_agent'
    }
  }
  environment{
    SFTP_HOST = "sftp.sero.ict.ericsson.net" 
    XDN_REPO = "10.145.159.150/nm-xdn/ccd-pipeline.git"
    MINIO_SERVER = "10.145.159.150"
    no_proxy = "10.145.159.150"
    VAULT_FILE = credentials('ccd_pipeline_secret')
  }
  // The options directive is for configuration that applies to the whole job.
  options {
    buildDiscarder(logRotator(numToKeepStr:'30'))
    timeout(time: 40, unit: 'MINUTES')
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
    stage('Run Pre-Requisites Check') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          sh "cd ccd_pipeline/capo_ansible; ansible-playbook -vvv -e deployment_id=${deployment_id} -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} --vault-password-file $VAULT_FILE check-and-upload-images-in-xdn.yml"
        }
      }
    }
  }
  // The post build actions
  post {
    always {
      cleanWs()
    }
    success {
      echo 'Pipeline Successfully Completed'
    }
    failure {
      echo 'Pipeline Failed'
    }
  }
}
