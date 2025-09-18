# JobHunter Pro

AI-Powered Multi-Platform Job Search application.

## Input Schema

The actor accepts the following parameters:
- `searchTerm` (required): Job title or keywords to search for
- `location`: Geographic location to search in
- `jobType`: Employment type (fulltime, parttime, contract, internship)
- `isRemote`: Boolean flag for remote-only positions
- `resultsWanted`: Number of results to return (10, 20, 50, or 100)
- `hoursOld`: Maximum age of job postings in hours
- `sources`: Array of job platforms to search

## Output

The actor returns an array of job objects with the following properties:
- id, title, company, location, salary_min, salary_max
- job_type, is_remote, posted_date, source, url, description