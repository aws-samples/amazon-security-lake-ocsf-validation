Amazon Security Lake Samples
========================

### AWS OCSF Samples 

In addition to the tool itself, several common  examples of AWS OCSF samples have been added to this repository under AWSLogs_OCSF_1.0.0-rc2_samples. These are pre-mapped OCSF compliant Amazon Security Lake supported log sources to provide as examples to users interested in mapping to OCSF.

Within the AWSLogs_OCSF_1.0.0-rc2_samples there are transformed parquet files and an inputs folder containing an original log record for each respective parquet file.

Running the validation tool using the provided samples will output the following:

### CloudTrail Account Change

	python validate.py -i path/to/AWSLogs_OCSF_1.0.0-rc2_samples/CLOUD_TRAIL/account_change
	[?] : ocsf_schema_1.0.0-rc.2
	 > ocsf_schema_1.0.0-rc.2

	Attempting to Validate File: AddroletoInstanceProfile.test.parquet...

	Validating Against Event Class: account_change (3001)...

	VALID OCSF.

	Attempting to Validate File: AttachRolePolicy.test.parquet...

	Validating Against Event Class: account_change (3001)...

	VALID OCSF.

	Attempting to Validate File: AttachUserPolicy.test.parquet...

	Validating Against Event Class: account_change (3001)...

	VALID OCSF.

	Attempting to Validate File: CreateRole.test.parquet...

	Validating Against Event Class: account_change (3001)...

	VALID OCSF.

	Attempting to Validate File: CreateServiceRole.test.parquet...

	Validating Against Event Class: account_change (3001)...

	VALID OCSF.

	Attempting to Validate File: CreateUser.test.parquet...

	Validating Against Event Class: account_change (3001)...

	VALID OCSF.

	Attempting to Validate File: DeleteRole.test.parquet...

	Validating Against Event Class: account_change (3001)...

	VALID OCSF.

### CloudTrail Generic API Activity

	python validate.py -i path/to/AWSLogs_OCSF_1.0.0-rc2_samples/CLOUD_TRAIL/generic_api_activity
	[?] : ocsf_schema_1.0.0-rc.2
	 > ocsf_schema_1.0.0-rc.2

	Attempting to Validate File: CreateLoadBalancer.test.parquet...

	Validating Against Event Class: api_activity (3005)...

	VALID OCSF.

	Attempting to Validate File: DeleteLoadBalancer.test.parquet...

	Validating Against Event Class: api_activity (3005)...

	VALID OCSF.

	Attempting to Validate File: DescribeDirectConnectGateways.test.parquet...

	Validating Against Event Class: api_activity (3005)...

	VALID OCSF.

	Attempting to Validate File: GetVpcLinks.test.parquet...

	Validating Against Event Class: api_activity (3005)...

	VALID OCSF.

	Attempting to Validate File: ListCloudFrontOriginAccessIdentities.test.parquet...

	Validating Against Event Class: api_activity (3005)...

	VALID OCSF.

	Attempting to Validate File: UnknownAPI.test.parquet...

	Validating Against Event Class: api_activity (3005)...

	VALID OCSF.

	Attempting to Validate File: UpdateTrail.test.parquet...

	Validating Against Event Class: api_activity (3005)...

	VALID OCSF.

### CloudTrail Authentication

	python validate.py -i path/to/AWSLogs_OCSF_1.0.0-rc2_samples/CLOUD_TRAIL/authentication
	[?] : ocsf_schema_1.0.0-rc.2
	 > ocsf_schema_1.0.0-rc.2

	Attempting to Validate File: AssumeRole.test.parquet...

	Validating Against Event Class: authentication (3002)...

	VALID OCSF.

	Attempting to Validate File: AssumeRoleWithSAML.test.parquet...

	Validating Against Event Class: authentication (3002)...

	VALID OCSF.

	Attempting to Validate File: AssumeRoleWithWebIdentity.test.parquet...

	Validating Against Event Class: authentication (3002)...

	VALID OCSF.

	Attempting to Validate File: CheckMfa.test.parquet...

	Validating Against Event Class: authentication (3002)...

	VALID OCSF.

	Attempting to Validate File: ConsoleLogin-mfa-failure.test.parquet...

	Validating Against Event Class: authentication (3002)...

	VALID OCSF.

	Attempting to Validate File: ConsoleLogin-mfa.test.parquet...

	Validating Against Event Class: authentication (3002)...

	VALID OCSF.

	Attempting to Validate File: ConsoleLogin.test.parquet...

	Validating Against Event Class: authentication (3002)...

	VALID OCSF.
	
### Route 53

	python validate.py -i path/to/AWSLogs_OCSF_1.0.0-rc2_samples/ROUTE53
	[?] : ocsf_schema_1.0.0-rc.2
	 > ocsf_schema_1.0.0-rc.2

	Attempting to Validate File: route53-0.json-transformed.parquet...

	Validating Against Event Class: dns_activity (4003)...

	VALID OCSF.

	Attempting to Validate File: route53-1.json-transformed.parquet...

	Validating Against Event Class: dns_activity (4003)...

	VALID OCSF.

	Attempting to Validate File: route53-2.json-transformed.parquet...

	Validating Against Event Class: dns_activity (4003)...

	VALID OCSF.

	Attempting to Validate File: route53-3.json-transformed.parquet...

	Validating Against Event Class: dns_activity (4003)...

	VALID OCSF.

### VPC Flow

	python validate.py -i path/to/AWSLogs_OCSF_1.0.0-rc2_samples/VPC_FLOW
	[?] : ocsf_schema_1.0.0-rc.2
	 > ocsf_schema_1.0.0-rc.2

	Attempting to Validate File: vpc_flow0.parquet...

	Validating Against Event Class: network_activity (4001)...

	VALID OCSF.

	Attempting to Validate File: vpc_flow1.parquet...

	Validating Against Event Class: network_activity (4001)...

	VALID OCSF.

	Attempting to Validate File: vpc_flow2.parquet...

	Validating Against Event Class: network_activity (4001)...

	VALID OCSF.

	Attempting to Validate File: vpc_flow3.parquet...

	Validating Against Event Class: network_activity (4001)...

	VALID OCSF.


### Security Hub Findings

	python validate.py -i path/to/AWSLogs_OCSF_1.0.0-rc2_samples/SH_FINDINGS
	[?] : ocsf_schema_1.0.0-rc.2
	 > ocsf_schema_1.0.0-rc.2

	Attempting to Validate File: securityhub0.json-transformed.parquet...

	Validating Against Event Class: security_finding (2001)...

	VALID OCSF.

	Attempting to Validate File: securityhub1.json-transformed.parquet...

	Validating Against Event Class: security_finding (2001)...

	VALID OCSF.

	Attempting to Validate File: securityhub2.json-transformed.parquet...

	Validating Against Event Class: security_finding (2001)...

	VALID OCSF.

	Attempting to Validate File: securityhub3.json-transformed.parquet...

	Validating Against Event Class: security_finding (2001)...

	VALID OCSF.


### Official Resources
- [Amazon Security Lake Overview](https://aws.amazon.com/security-lake/)
- [Amazon Security Lake Custom Data](https://docs.aws.amazon.com/security-lake/latest/userguide/custom-sources.html)
- [OCSF Schema Browser](https://schema.ocsf.io/)

# License <a name="License"></a>

This library is licensed under the MIT-0 License.
		







