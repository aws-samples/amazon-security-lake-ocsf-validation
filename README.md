Amazon Security Lake Resources
========================

## Table of Contents
1. [About this Repo](#About)
2. [License](#License)
3. [Validation Tool](#Validation)
4. [AWS OCSF Samples](#samples)

## About this Repo <a name="About"></a>

This repo is a collection of resources which are supplemental to Amazon Security Lake. Amazon Security Lake automatically centralizes security data from cloud, on-premises, and custom sources into a purpose-built data lake stored in your account. With Security Lake, you can get a more complete understanding of your security data across your entire organization. You can also improve the protection of your workloads, applications, and data. Security Lake has adopted the Open Cybersecurity Schema Framework (OCSF), an open standard. With OCSF support, the service can normalize and combine security data from AWS and a broad range of enterprise security data sources. 

The resources currently available within this repo are as follows:

1. [OCSF Parquet Data Validation](https://github.com/aws-samples/amazon-security-lake/tree/main/validate_1.0.0-rc.2)
2. [AWS OCSF Samples](https://github.com/aws-samples/amazon-security-lake/tree/main/AWSLogs_OCSF_1.0.0-rc2_samples)

We welcome contributions to this repo in the form of fixes to existing examples or addition of new examples. For more information on contributing, please see the [CONTRIBUTING](https://github.com/aws-samples/amazon-security-lake/blob/main/CONTRIBUTING.md) guide.

### Validation Tool <a name="Validation"></a>

The following is a simple program which can be used to ensure that user provided parquet data properly maps to the various schema definitions specified within the Open Cyber Security Framework (OCSF) - https://schema.ocsf.io/.

This tool was build to provide supplementry validation for Amazon Security Lake which requires data to be in the format specified by OCSF Schema 1.0.0-rc.2.

### AWS OCSF Samples <a name="samples"></a>

In addition to the tool itself, several common  examples of AWS OCSF samples have been added to this repository under AWSLogs_OCSF_1.0.0-rc2_samples. These are pre-mapped OCSF compliant Amazon Security Lake supported log sources to provide as examples to users interested in mapping to OCSF.

 Attempting to Validate File: AssumeRoleWithSAML.test.parquet...
 Validating Against Event Class: authentication (3002)...
 
 VALID OCSF.
 
 Attempting to Validate File: AssumeRoleWithWebIdentity.test.parquet...
 Validating Against Event Class: authentication (3002)...
 
 VALID OCSF.
 
 Attempting to Validate File: AttachRolePolicy.test.parquet...
 Validating Against Event Class: account_change (3001)...
 
 VALID OCSF.
 
 Attempting to Validate File: AttachUserPolicy.test.parquet...
 Validating Against Event Class: account_change (3001)...
 
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
 
 Attempting to Validate File: CreateRole.test.parquet...
 Validating Against Event Class: account_change (3001)...
 
 VALID OCSF.
 
 Attempting to Validate File: CreateServiceRole.test.parquet...
 Validating Against Event Class: account_change (3001)...
 
 VALID OCSF.
 
 Attempting to Validate File: CreateUser.test.parquet...
 Validating Against Event Class: account_change (3001)...
 
 VALID OCSF.
 
 Attempting to Validate File: DeleteLoadBalancer.test.parquet...
 Validating Against Event Class: api_activity (3005)...
 
 VALID OCSF.
 
 Attempting to Validate File: DeleteRole.test.parquet...
 Validating Against Event Class: account_change (3001)...
 
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
 
 Attempting to Validate File: route53-1.json-transformed.parquet...
 Validating Against Event Class: dns_activity (4003)...
 
 VALID OCSF.
 
 Attempting to Validate File: route53-2.json-transformed.parquet...
 Validating Against Event Class: dns_activity (4003)...
 
 VALID OCSF.
 
 Attempting to Validate File: route53-3.json-transformed.parquet...
 Validating Against Event Class: dns_activity (4003)...
 
 VALID OCSF.
 
 Attempting to Validate File: UnknownAPI.test.parquet...
 Validating Against Event Class: api_activity (3005)...
 
 VALID OCSF.
 
 Attempting to Validate File: UpdateTrail.test.parquet...
 Validating Against Event Class: api_activity (3005)...
 
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
		







