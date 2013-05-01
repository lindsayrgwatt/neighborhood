from fabric.api import local

def prepare_deployment():
    local('python manage.py test hoods --settings=neighborhood.settings.local')
    local('git add -A && git commit')
    local('git push origin master')
    