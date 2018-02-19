#!/bin/bash
#CREATE THE DATABASE
#deprecated
#curl -G 'http://localhost:8086/query' --data-urlencode "q=create database python_response_time"
curl -XPOST http://localhost:8086/query --data-urlencode 'q=CREATE DATABASE "python_response_time"'
