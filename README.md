Amazon Security Lake Data Validation 
========================

## Table of Contents
1. [About this Repo](#About)
2. [Usage Guide](#Usage)
3. [Examples](#Examples)
4. [License](#License)
5. [Checksum](#Checksum)

## About this Repo <a name="About"></a>

The following is a simple program which can be used to ensure that user provided parquet data properly maps to the various schema definitions specified within the Open Cyber Security Framework (OCSF) - https://schema.ocsf.io/. 

This tool was build to provide supplementry validation for Amazon Security Lake which requires data to be in the format specified by OCSF Schema 1.0.0-rc.2. 

We welcome contributions to this repo in the form of fixes to existing examples or addition of new examples. For more information on contributing, please see the [CONTRIBUTING](https://github.com/aws-samples/amazon-security-lake/blob/main/CONTRIBUTING.md) guide.


## Usage Guide <a name="Usage"></a>

To get started with using this validator please follow the numbered steps below:

1. Please place parquet files in: path/to/inputs
    
3. Install requirements using 
        pip install -r requirements.txt

4. This script will throw error without installation of most current version of packages specified in step 2

5. Run

		python validate.py -i "path/to/inputs" -version ocsf_schema_1.0.0-rc.2
		



## Examples <a name="Examples"></a>

Below we can see an expected validation result by executing the script in the samples folder: path/to/samples/sample.py

	python sample.py

The expected output from running the sample is as follows:

		Validating Against Event Class: api_activity (3005)...

		----------------------------------------FILE DATA----------------------------------------
		{
		      "activity_id": 2,
		      "activity_name": "Read",
		      "api": {
			    "operation": "PutObject",
			    "request": {
				  "uid": "AAAAA1111BBBB222"
			    },
			    "service": {
				  "name": "s3.amazonaws.com"
			    }
		      },
		      "actor": { 

		....
		....
		....

		-------------------------------------------------------------------------------------

		VALID OCSF.

## Checksum <a name="Checksum"></a>

To ensure the soundness of the download, you may choose run a checksum against the files in this repository. You can verify the integrity of the validate.py by ensuring the shasum (SHA-256) matches the following:

	cf67afaf295e74651f7de803fc96ee1cab3e5502a9896ceb835aabbf4e14af88

### Official Resources
- [Amazon Security Lake Overview](https://aws.amazon.com/security-lake/)
- [Amazon Security Lake Custom Data](https://docs.aws.amazon.com/security-lake/latest/userguide/custom-sources.html)
- [OCSF Schema Browser](https://schema.ocsf.io/)

# License <a name="License"></a>

This library is licensed under the MIT-0 License.
