heroku pgbackups:capture --expire --app barberscore-api
heroku pgbackups:restore DATABASE `heroku pgbackups:url --app barberscore-api` \
--app barberscore-api-staging --confirm barberscore-api-staging
