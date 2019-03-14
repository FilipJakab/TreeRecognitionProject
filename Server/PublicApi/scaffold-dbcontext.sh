#!/bin/bash

connectionString=$(cat "./PublicApi/ConnectionStrings.json" | jq .ConnectionStrings.TreeRecognitionDb | cat)

#echo $connectionString

dotnet ef dbcontext scaffold $connectionString Microsoft.EntityFrameworkCore.SqlServer --startup-project PublicApi --project PublicApi.Database -f
