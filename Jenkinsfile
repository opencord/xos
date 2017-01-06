node ('build') {
    stage('Config') {
        sh '$TARGET_MACHINE_SSH_COMMAND "\
        cd ~/opencord; \
        echo $GERRIT_BRANCH; \
        /home/sdn/bin/repo checkout $GERRIT_BRANCH; \
        /home/sdn/bin/repo sync; \
        echo $GERRIT_PROJECT; \
        if [ "$GERRIT_PROJECT" = "service-profile" ]; then cd orchestration/service-profile/; fi; \
        if [ "$GERRIT_PROJECT" = "xos" ]; then cd orchestration/xos/; fi; \
        git fetch opencord $GERRIT_REFSPEC:$CHANGE_BRANCH; \
        git checkout $CHANGE_BRANCH" '
    }
    stage('Build') {
        sh '$TARGET_MACHINE_SSH_COMMAND "\
        cd ~/opencord/orchestration/service-profile/frontend; \
        make rm; \
        make local_containers; \
        make" '
    }
    stage('Test') {
        sh '$TARGET_MACHINE_SSH_COMMAND "\
        cd ~/opencord/test/cord-tester/src/test/cord-api/Properties/; \
        cp RestApiProperties.py RestApiProperties.py.copy; \
        sed -i $SET_SERVER_IP_COMMAND RestApiProperties.py; \
        sed -i $SET_SERVER_PORT_COMMAND RestApiProperties.py; \
        cd ~/opencord/test/cord-tester/src/test/cord-api/Tests/; \
        rm -r ../Log; \
        pybot -d ../Log -T ServiceTest.txt; \
        pybot -d ../Log -T Users.txt; \
        pybot -d ../Log -T UtilsSynchronizer.txt; \
        pybot -d ../Log -T DeploymentTest.txt; \
        pybot -d ../Log -T SanityNode.txt; \
        pybot -d ../Log -T SanitySlice.txt; \
        pybot -d ../Log -T SanityInstance.txt; \
        pybot -d ../Log -T SanityFlavors.txt; \
        cd ~/opencord/test/cord-tester/src/test/cord-api/Properties/; \
        mv RestApiProperties.py.copy RestApiProperties.py; \" '
    }
    stage('Publish') {
        sh 'rm -r RobotLogs; mkdir RobotLogs'
        sh 'sshpass -p $TARGET_MACHINE_PASSWORD scp -r $TARGET_MACHINE_USERNAME@$TARGET_MACHINE_IP:~/opencord/test/cord-tester/src/test/cord-api/Log/* ./RobotLogs'
        step([$class: 'RobotPublisher',
            disableArchiveOutput: false,
            logFileName: 'RobotLogs/log*.html',
            otherFiles: '',
            outputFileName: 'RobotLogs/output*.xml',
            outputPath: '.',
            passThreshold: 100,
            reportFileName: 'RobotLogs/report*.html',
            unstableThreshold: 0]);
    }
}
