## gcdt-lookups plugin

The lookups functionality is pinned to a dedicated gcdt lifecycle step. 


### Related documents

* [credstash](https://github.com/fugue/credstash)


### lookup stack output

The `stack` lookup is used to substitute configuration where the value is an output from another cloudformation stack.

```eval_rst
+---------+-------------------------------------+
| format: | `lookup:stack:<stackname>:<output>` |
+---------+-------------------------------------+
| sample: | `lookup:secret:slack.webhook`       |
+---------+-------------------------------------+
```

regional lookup of stack output:
```eval_rst
+---------+-----------------------------------------------------+
| format: | `lookup:region:<region>:stack:<stackname>:<output>` |
+---------+-----------------------------------------------------+
| sample: | `lookup:region:us-east-1:secret:slack.webhook`      |
+---------+-----------------------------------------------------+
```


### DEPRECATED lookup ssl certificate

```eval_rst
+---------+-----------------------------------------------------+
| format: | `lookup:ssl:<stackname>:<output>`                   |
+---------+-----------------------------------------------------+
| sample: | `lookup:ssl:*.infra.glomex.cloud`                   |
+---------+-----------------------------------------------------+
```

'ssl' lookup uses the `server_certificate` functionality built into AWS IAM. It is configured default lookup so for each stack also the certificates are added to stackdata.

This is DEPRECATED! If possible, please use the acm lookup!


### lookup acm certificate

```eval_rst
+---------+-----------------------------------------------------------------------------------------+
| format: | `lookup:acm:<name_1>:...:<name_n>:`                                                     |
+---------+-----------------------------------------------------------------------------------------+
| sample: | `lookup:acm:foo.mes.glomex.cloud:supercars.infra.glomex.cloud:*.dev.infra.glomex.cloud` |
+---------+-----------------------------------------------------------------------------------------+
```

'acm' lookup uses the AWS ACM (Certificate Manager) functionality. It is configured as default lookup.

Features of the `acm lookup`:

* pass a list of hostnames that should be secured.
* check all certificates in ACM if the configured CN (DomainName) or SANs (SubjectAlternativeNames) (including wildcards) if they match for the given list of hostnames
* the chosen certificates STATUS must be **ISSUED**
* if there are multiple matches, use the one with the most distant expiry date
* return the ARN of the certificate
* wildcards for hosted zone are expressed with "*."
* 'ERROR' in case a certificate matching the specified list of names can not be found

Note: if you use ACM lookup in yugen / API Gateway you need to deploy the certificates to the `us-east-1` region.


### lookup secret

The `secret` lookup is used to substitute configuration where the value is a password, token or other sensitive information that you can not commit to a repository.  
 
lookup the 'datadog_api_key' entry from credstash:
```eval_rst
+---------+-----------------------------------------------------+
| format: | `lookup:secret:<name>.<subname>`                    |
+---------+-----------------------------------------------------+
| sample: | `lookup:secret:datadog.api_key`                     |
+---------+-----------------------------------------------------+
```

regional lookup of secret:
```eval_rst
+---------+-----------------------------------------------------+
| format: | `lookup:region:<region>:secret:<name>.<subname>`    |
+---------+-----------------------------------------------------+
| sample: | `lookup:region:us-east-1:secret:datadog.api_key`    |
+---------+-----------------------------------------------------+
```

lookup the 'slack.webhook' entry from credstash:
```eval_rst
+---------+-----------------------------------------------------+
| sample: | `lookup:secret:slack.webhook:CONTINUE_IF_NOT_FOUND` |
+---------+-----------------------------------------------------+
```

note that the `slack.webhook` lookup does not fail it the accounts credstash does not have the `slack.token` entry.


### DEPRECATED lookup baseami

The `baseami` lookup is used lookup the baseami for cloudformation infrastructures.
