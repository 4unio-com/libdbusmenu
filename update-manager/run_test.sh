#!/bin/bash

if [ $# -ne 1 ];
then
    echo "Syntax: ./run_open_test.sh <XML file>."
    exit 0
fi

if [ ! -r $1 ];
then
    echo "The XML file" $1 "cannot be read."
    exit 0
fi

ldtprunner $1 

length=$((${#1} - 4))
report="${1:0:length}"".html"

xsltproc -o $report report.xsl temp_log.xml

firefox $report &

exit 0

