# Network Data Analysis (A data driven analysis on top-500 most visited sites)

This project includes a collection of mostly python scripts for analysis of top-500 most visited domains on the WWW. The code provide the following functionalities:
- Collect the list of most visited top sites from `www.alexa.com/topsites`.
- Collect details of response time about the download of the front page of a list of domain, using **curl**.
- Collect HAR (HTTP Archive) log of a domain using **PhantomJS**
- Analyze the URI of individual data objects in HAR log of a web-page, and see whether it is served from a CDN.

A few **IPython Notebooks** are also included to analyze the collected data and create illustrative figures using *matplotlib* and *Pandas*.
