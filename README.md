# sonarscan
A subdomain scanner that uses Rapid7's FDNS datasets to identify CNAME records/subdomains in a domain. It automatically downloads the latest version of the dataset and searches for the queried string in the dataset.

Subdomain takeover vulnerabilities occur when a subdomain of a website (subdomain.example.com) is pointing to a service (e.g. AWS S3, GitHub pages, Heroku, etc.) that has been removed or deleted. This allows an attacker to set up a page on the service that was being used and point their page to that subdomain. For example, if subdomain.example.com was pointing to a Amazon AWS S3 Bucket and the user decided to delete their S3 bucket, an attacker can now create a S3 bucket with the same name, or add a CNAME file containing subdomain.example.com, and claim subdomain.example.com.

The tool is in its initial stages. Appreciate everybody's feedback.
