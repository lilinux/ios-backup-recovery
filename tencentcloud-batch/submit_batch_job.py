import os
import json

# custom (Change to your info)
name = 'pang'
dicts = 'digits_4.txt digits_6.txt'
crack_file = '%s.plist' % name
task_num = 100
imageId = "img-31tjrtph"    # image must installed cloud-init and configured
cos_url = 'cos://YOUR-COS-URL'

# Task config(ComputeEnv)
ComputeEnv = {
    "EnvType": "MANAGED",
    "EnvData": {
        "InstanceType": "C3.2XLARGE32",
        "ImageId": imageId,
        "SystemDisk": {
            "DiskType": "CLOUD_BASIC",
            "DiskSize": 50
        },
    }
}

# Task config(RedirectInfo stdout & stderr)
RedirectInfo = {
    "StdoutRedirectPath": "%s/logs/" % cos_url,
    "StderrRedirectPath": "%s/logs/" % cos_url,
}      

bruteforce_job = {
    "JobName": "BruteForceJob",
    "JobDescription": "for test",
    "Priority": "1",
    "Dependences": [
      {
        'StartTask': 'split',
        'EndTask': 'crack',
      }
    ],
    "Tasks": [
        {
            "TaskName": "split",
            "TaskInstanceNum": 1,
            "Application": {
              "DeliveryForm": "PACKAGE",
              "Command": "python ./split/split.py %s %s" % (task_num, dicts),
              "PackagePath": '%s/pkg/split.tgz' % cos_url,
            },
            "ComputeEnv": ComputeEnv,
            "InputMappings": [
              {
                "SourcePath": "%s/dictionarys/" % cos_url,
                "DestinationPath": "/root/dicts/",
              }
            ],
            "OutputMappings": [
              {
                "SourcePath": "/root/split_dicts/",
                "DestinationPath": "%s/input/" % cos_url,
              }
            ],
            "RedirectInfo": RedirectInfo,
        },
        {
            "TaskName": "crack",
            "TaskInstanceNum": task_num,
            "Application": {
              "DeliveryForm": "PACKAGE",
              "Command": "python ./crack/main.py /root/input/%s" % crack_file,
              "PackagePath": '%s/pkg/crack.tgz' % cos_url,
            },
            "ComputeEnv": ComputeEnv,
            "InputMappings": [
              {
                "SourcePath": "%s/input/" % cos_url,
                "DestinationPath": "/root/input/",
              }
            ],
            "OutputMappings": [
              {
                "SourcePath": "/root/output/",
                "DestinationPath": "%s/output/" % cos_url,
              }
            ],
            "RedirectInfo": RedirectInfo,
        }
    ]
}

cmd= "qcloudcli batch SubmitJob \
    --Version 2017-03-12 \
    --Placement '{\"Zone\": \"ap-guangzhou-3\"}' \
    --Job ' %s ' "%(json.dumps(bruteforce_job))
os.system(cmd)

