docker build -t  pyspark_test

docker run pyspark_test driver local:///opt/application/main.py  {{args}}


 