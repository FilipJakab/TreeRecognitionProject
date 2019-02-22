#!/bin/bash

variables=$(dotnet user-secrets list --project PublicApi)
key='ConnectionStrings:TreeRecognitionDb = '
keyLen=$(echo $key | wc -m)


IFS=$'\n'
for line in $variables
do
	if [[ $line == $key* ]];
	then
		connectionString=${line:$keyLen:$(echo $line | wc -m)}
	fi
done

# echo "$connectionString"

dotnet ef dbcontext scaffold "$connectionString" Microsoft.EntityFrameworkCore.SqlServer --startup-project PublicApi --project PublicApi.Database -f
