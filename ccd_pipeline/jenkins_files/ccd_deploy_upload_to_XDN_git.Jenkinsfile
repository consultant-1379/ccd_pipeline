pipeline {
  agent {
    node {
      label 'XDN_SLAVE'
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
               currentBuild.displayName = "${env.BUILD_NUMBER}"
          }
      }
    }
    stage('Checkout XDN repo'){
        steps{
            withCredentials([usernamePassword(credentialsId: 'jenkins_gitlab', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USER')]) {
                checkoutXDNrepo("${XDN_REPO}","${GIT_USER}", "${GIT_PASSWORD}")
            }
        }
    }

    stage('GET FROM SFTP') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'xdn_sftp', passwordVariable: 'SFTP_PASSWORD', usernameVariable: 'SFTP_USER')]) {
          getFromSftp("${SFTP_USER}", "${SFTP_PASSWORD}", "${SFTP_HOST}", "ccd-pipeline")
          getMinioFilesFromSftp("${SFTP_USER}", "${SFTP_PASSWORD}", "${SFTP_HOST}", "/tmp")
        }
      }
    }

    stage ("PUT to XDN MINIO"){
        steps{
            withCredentials([usernamePassword(credentialsId: 'xdn_minio', passwordVariable: 'MINIO_PASSWORD', usernameVariable: 'MINIO_USER')]) {
                putToMinio("${MINIO_USER}", "${MINIO_PASSWORD}")
            }

        }
    }

    stage ("PUSH to XDN REPO"){
        steps{
            withCredentials([usernamePassword(credentialsId: 'jenkins_gitlab', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USER')]) {
                unpackAndPush("${XDN_REPO}","${GIT_USER}", "${GIT_PASSWORD}")
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
    always {
        cleanWs()
    }
  }
}

def checkoutXDNrepo(String repo, String user,String password){
    sh"""
        git -c http.proxy="" clone "http://$user:$password@$repo"
    """
}


def getFromSftp(String user,String password,String host,String dir ){
  sh"""
  lftp -u $user,$password -e 'set sftp:connect-program "ssh -o StrictHostKeyChecking=no";get ccd_pipeline/repo/repo.tgz -o $dir/repo.tgz;exit' sftp://$host
  """
}

def getMinioFilesFromSftp(String user,String password,String host,String dir ){
  sh"""
  lftp -u $user,$password -e 'set sftp:connect-program "ssh -o StrictHostKeyChecking=no";mirror ccd_pipeline/minio/ $dir/minio/;exit'  sftp://$host
  ls -lahR $dir/minio/
  """
}

def putToMinio(String user, String password){
  sh"""
docker run --rm -t -v /tmp/minio/cloud/:/data --entrypoint=/bin/sh minio/mc -c "mc alias set myminio http://${MINIO_SERVER}:9000 $user $password && mc cp --recursive /data/* myminio/templates/cloud"
rm -rf /tmp/minio/cloud

list=\$(ls /tmp/minio/managed-config/ | sed 's/\\(.*\\)\\.capo\\.env\\.yml/\\1/; s/\\(.*\\)\\.env\\.yml/\\1/; s/\\(.*\\)\\.template\\.yml/\\1/; s/\\(.*\\)\\.yml/\\1/' | uniq)
echo \$list

for item in \$list; do
  docker run --rm -t -v /tmp/minio/managed-config/:/data --entrypoint=/bin/sh minio/mc -c "mc alias set myminio http://${MINIO_SERVER}:9000 $user $password && mc cp --recursive /data/\$item* myminio/templates/managed-config/\$item/"
done
rm -rf /tmp/minio/managed-config/
  """
}

def unpackAndPush(String repo, String user,String password){
    sh"""cd ccd-pipeline
        git config --global user.name "Jenkins User"
        git config --global user.email "jenkins@example.com"
        tar xvf repo.tgz
        rm repo.tgz
        git add .
        if git diff --cached --exit-code; then
            echo "No changes to commit."
        else
            git commit -m "UPDATE from build: ${env.BUILD_NUMBER}"
            git -c http.proxy="" push -q "http://$user:$password@$repo"
        fi 
    """
}