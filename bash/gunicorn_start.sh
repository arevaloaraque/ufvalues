#!/bin/bash

NAME="ufvalues"
USER="ufvalues"
BASE_FOLDER=/webapps/$USER
DJANGODIR=$BASE_FOLDER/
SOCKFILE=$DJANGODIR/env/run/gunicorn.sock
TIMEOUT=600
GROUP=ufvalues
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=microservicio_valor_uf.settings
DJANGO_WSGI_MODULE=microservicio_valor_uf.wsgi
VIRTUALENV_BIN=$DJANGODIR/env/bin
NOW=$(date +'%d/%m/%Y %T')

echo "[$NOW] STARTING GUNICORN PROJECT $NAME AS `whoami` USER"
cd $DJANGODIR/
source $VIRTUALENV_BIN/activate
echo "[$NOW] ACTIVATING VIRTUALENV $VIRTUEALENV_BIN"
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
echo  "[$NOW] EXPORTING DJANGO PROJECT $DJANGODIR"
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

echo "[$NOW] GENERATING SOCKECT FILE $SOCKFILE"
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

#Start gunicorn
exec $VIRTUALENV_BIN/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --timeout=$TIMEOUT \
    --user $USER \
    --group $GROUP \
    --bind unix:$SOCKFILE \
    --log-level info \
    --log-file logs/gunicorn.log

