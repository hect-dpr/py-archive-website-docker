# Archive Website - Python/Docker
Docker container with a command line program that can fetch entire web pages with assets and saves them to disk for later retrieval and browsing and displays last fetch metadata.

## Steps to Run
- Clone/ download repo, install Docker cd to directory with Dockerfile and run:
```
docker build -t py-archive-website .
docker run -dt --name py-archive-website -v <full local machine path>:/root/fetch py-archive-website
docker exec -it py-archive-website bash
```
- Inside the container terminal on running the following command, the respective htmls, assets(css, img, script), metadata(txt) will be saved and is also accessible in the \<full local machine path\>:
```
$> ./fetch.py https://www.google.com https://yahoo.com <...> (we can specify multiple URLs)
$> ls
yahoo.com.html yahoo.com_assets yahoo.com.txt www.google.com.html www.google.com_assets www.google.com.txt
```
- Example for retrieving metadata:
```
$> ./fetch.py --metadata https://www.google.com <...> (also chainable)
site: www.google.com
num_links: 35
images: 3
last_fetch: Tue Mar 16 2021 15:46 UTC
```
