
kubectl create secret generic mysql-secret `
>>   --from-literal=root-password=test `
>>   --from-literal=database=planner_db `
>>   --from-literal=user=test `
>>   --from-literal=password=test

kubectl create secret generic fastapi-env --from-env-file=./fastapiEnv/.env

kubectl apply -R -f .  