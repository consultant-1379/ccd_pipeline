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
  environment{
    SFTP_HOST = "sftp.sero.ict.ericsson.net" 
    XDN_REPO = "10.145.159.150/nm-xdn/ccd-pipeline.git"
    MINIO_SERVER = "10.145.159.150"
    no_proxy = "10.145.159.150"
  }
  stages {
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
          sh "cd ccd_pipeline/ansible; ansible-playbook -e deployment_id=${deployment_id}  -e sftp_user=${SFTP_USER} -e sftp_password=${SFTP_PASSWORD} deploy-ccd-stack-xdn.yml -vvv"
        }
      }
    }

    // stage('Run deployment Healthcheck') {
    //   steps {
    //     sh "cd ccd_pipeline/ansible; ansible-playbook -e deployment_id=${deployment_id} healthcheck.yml -vvv"
    //   }
    // }

    // stage ('Add CCD to monitoring'){
    //   steps{
    //     echo "Running add_to_monitoring"
    //     build job: 'add_to_monitoring', parameters: [string(name: 'deployment_id', value: "${params.deployment_id}")]
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
