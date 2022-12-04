docker-compose exec -T matchanalysis-django isort .
docker-compose exec -T matchanalysis-django flake8 .
docker-compose exec -T matchanalysis-django black .

sudo chown -R $USER:$USER .