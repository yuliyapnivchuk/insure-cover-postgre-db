First run below command to build the image based on Dockerfile

``` docker build -t ic_postgre . ```


Then start docker container with command below. 

``` docker run ic_postgre ```


temporary solution 

``` docker pull postgres ```

``` docker run --name insure-cover -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=ic -p 5432:5432 -d postgres ```