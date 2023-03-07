Usage Guide
========================

1. please place parquet files in: path/to/inputs

2. depends on installation of following python packages:
		path
		jsonschema
		pandas
		urllib
        requests
        pathlib
        importlib

    
3. Install requirements using 
        pip install -r requirements.txt

4. this script will throw error without installation of most current version of packages specified in step 2

5. run

		python validate.py -i "path/to/inputs" -version ocsf_schema_1.0.0-rc.2
		
NOTE: See expected output by executing path/to/samples/sample.py



\C:\Users\adplotzk\Desktop\amazon-security-lake\validate_1.0.0-rc.2\sample>python sample.py

The output from running the sample is as follows:

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
