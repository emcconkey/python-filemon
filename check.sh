#!/bin/bash

export START_FOLDER=$(grep start_folder efw.ini | cut -d '=' -f 2)
export SAVE_FOLDER=$(grep save_folder efw.ini | cut -d '=' -f 2)
export EMAIL_FROM=$(grep email_from efw.ini | cut -d '=' -f 2)
export EMAIL_TO=$(grep email_to efw.ini | cut -d '=' -f 2)

ls -laR ${START_FOLDER} > ${SAVE_FOLDER}/filelist.txt

./efw.py > ${SAVE_FOLDER}/notifications.txt

fsize=$(wc -l < ${SAVE_FOLDER}/notifications.txt)

if ((fsize<1)); then
    echo "No changes detected";
else
    echo "Filesystem changes detected:";
    cat ${SAVE_FOLDER}/notifications.txt
    echo To: ${EMAIL_TO} > mail.txt
    echo From: ${EMAIL_FROM} >> mail.txt
    echo Subject: ${HOSTNAME} Filesystem Change Alert >> mail.txt
    echo >> mail.txt
    echo "The following changes have been detected in the filesystem" >> mail.txt
    cat ${SAVE_FOLDER}/notifications.txt >> mail.txt
    ssmtp ${EMAIL_TO} < ${SAVE_FOLDER}/mail.txt
    date >> ${SAVE_FOLDER}/log.txt
    echo "Sent email to ${EMAIL_TO}" >> ${SAVE_FOLDER}/log.txt
    cat ${SAVE_FOLDER}/notifications.txt >> ${SAVE_FOLDER}/log.txt
fi
