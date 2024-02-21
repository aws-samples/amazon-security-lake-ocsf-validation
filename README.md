Amazon Security Lake Resources
========================

## Table of Contents
1. [About this Repo](#About)
2. [Usage Guide](#Usage)
3. [License](#License)
4. [Validation Tool](#Validation)
5. [AWS OCSF Samples](#samples)

## About this Repo <a name="About"></a>

The following is a simple program which can be used to ensure that user provided parquet data properly maps to the various schema definitions specified within the Open Cyber Security Framework (OCSF) - https://schema.ocsf.io/. 

This tool was build to provide supplementry validation for Amazon Security Lake which requires data to be in the format specified by OCSF Schema 1.0.0-rc.2 or 1.1.0.

We welcome contributions to this repo in the form of fixes to existing examples or addition of new examples. For more information on contributing, please see the [CONTRIBUTING](https://github.com/aws-samples/amazon-security-lake/blob/main/CONTRIBUTING.md) guide.


## Usage Guide <a name="Usage"></a>

### Important Information for MacOs Users:
For users attempting to run this tool using MacOS please ensure that you are not using the default system version of Python. MacOS system python is incompatibile with the required urllib dependency within this tool.

To get started with using this validator please follow the numbered steps below:

1. Please place .parquet or .json files in: path/to/directory

2. OPTIONAL: Place .source files in path/to/directory/inputs/. These source files should be the json formatted records formatted in their original schema before OCSF. All source files must contain a the same name as the input file with a .source extension such as <inputfilename>.source to be used in metrics output. 
    
3. Install requirements using 
        pip install -r requirements.txt

4. This script will throw error without installation of most current version of packages specified in step.

5. Run

		python validate.py -i <path/to/directory>
		
		usage: validate.py [-h] -i INPUT

		options:
		  -h, --help            Show help.

		required arguments:
		  -i INPUT, --input INPUT
		

## Examples <a name="Examples"></a>

Below we can see an expected validation result for an INVALID ocsf record by executing the script in the samples folder: /path/to/amazon-security-lake-ocsf-validation/samples/1.1.0/EKS

The expected output from running the sample is as follows:

		-------- ATTEMPTING TO VALIDATE FILE:  UpdateTrail.parquet--------

		Validating Against OCSF Event Class: 6003
		Validating Against OCSF Version: 1.1.0
		Validating Against OCSF Profiles: ['cloud', 'datetime']

		------------------------------- INPUT RECORD ------------------------------

		{
			  "metadata": {
					"product": {
						  "version": "1.04",
						  "name": "CloudTrail",
						  "vendor_name": "AWS",
						  "feature": {
								"name": "Management, Data, and Insights"
						  }
					},
					"event_code": "AwsApiCall",
					"uid": "b7d4398e-b2f0-4faa-9c76-e2d316a8d67f",
					"profiles": [
						  "cloud",
						  "datetime"
					],
					"version": "1.1.0"
			  },
			  "time": 1468523745000,
			  "time_dt": 1468523,
			  "cloud": {
					"region": "us-east-2",
					"provider": "AWS"
			  },
			  "api": {
					"response": {
						  "error": "TrailNotFoundException",
						  "message": "Unknown trail: myTrail2 for the user: 111122223333"
					},
					"operation": "UpdateTrail",
					"service": {
						  "name": "cloudtrail.amazonaws.com"
					},
					"request": {
						  "uid": "5d40662a-49f7-11e6-97e4-d9cb6ff7d6a3"
					}
			  },
			  "actor": {
					"user": {
						  "type": "IAMUser",
						  "name": "Alice",
						  "uid_alt": "EX_PRINCIPAL_ID",
						  "uid": "arn:aws:iam::111122223333:user/Alice",
						  "account": {
								"uid": "111122223333"
						  },
						  "credential_uid": "EXAMPLE_KEY_ID"
					}
			  },
			  "http_request": {
					"user_agent": "aws-cli/1.10.32 Python/2.7.9 Windows/7 botocore/1.4.22"
			  },
			  "src_endpoint": {
					"ip": "205.251.233.182"
			  },
			  "class_name": "API Activity",
			  "class_uid": 6003,
			  "category_name": "Application Activity",
			  "category_uid": 6,
			  "severity_id": 1,
			  "severity": "Informational",
			  "status": "Failure",
			  "activity_name": "Update",
			  "activity_id": 3,
			  "type_uid": 600303,
			  "type_name": "API Activity: Update",
			  "unmapped": {
					"recipientAccountId": "111122223333",
					"requestParameters.name": "myTrail2"
			  }
		}


		---------------------------------- OUTPUT ---------------------------------

		INVALID OCSF.

		1468523 is not of type 'string'

		Failed validating 'type' in schema['properties']['time_dt']:
			{'title': 'Event Time', 'type': 'string'}

		On instance['time_dt']:
			1468523


		--------------------------------- METRICS ---------------------------------

		WARN: The OCSF log has: 5.13% of its keys in unmapped.
		WARN: The following number of source keys: 1 were not found in the transformed data...

		{
			"eventTime": "2016-07-14T19:15:45Z"
		}



## Checksum <a name="Checksum"></a>

To ensure the soundness of the download, you may choose run a checksum against the files in this repository. You can verify the integrity of the validate.py by ensuring the shasum (SHA-256) matches the following:

	cf67afaf295e74651f7de803fc96ee1cab3e5502a9896ceb835aabbf4e14af88


We welcome contributions to this repo in the form of fixes to existing examples or addition of new examples. For more information on contributing, please see the [CONTRIBUTING](https://github.com/aws-samples/amazon-security-lake/blob/main/CONTRIBUTING.md) guide.

### Validation Tool <a name="Validation"></a>

The following is a simple program which can be used to ensure that user provided parquet data properly maps to the various schema definitions specified within the Open Cyber Security Framework (OCSF) - https://schema.ocsf.io/.

This tool was build to provide supplementry validation for Amazon Security Lake which requires data to be in the format specified by OCSF Schema 1.0.0-rc.2.

### AWS OCSF Samples <a name="samples"></a>

In addition to the tool itself, several common  examples of AWS OCSF samples have been added to this repository under AWSLogs_OCSF_1.0.0-rc2_samples. These are pre-mapped OCSF compliant Amazon Security Lake supported log sources to provide as examples to users interested in mapping to OCSF.

### Official Resources
- [Amazon Security Lake Overview](https://aws.amazon.com/security-lake/)
- [Amazon Security Lake Custom Data](https://docs.aws.amazon.com/security-lake/latest/userguide/custom-sources.html)
- [OCSF Schema Browser](https://schema.ocsf.io/)

# License <a name="License"></a>

This library is licensed under the MIT-0 License.


Amazon Security Lake Data Validation 
========================

## Table of Contents
1. [About this Repo](#About)
2. [Usage Guide](#Usage)
3. [Examples](#Examples)
4. [License](#License)
5. [Checksum](#Checksum)
