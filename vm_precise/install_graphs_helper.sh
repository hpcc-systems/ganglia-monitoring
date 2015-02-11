#!/bin/bash

# Prerequistes
# apt-get install ganglia-webfrontend gmetad ganglia-monitor python-lxml collectd-core libltdl7 libganglia1 libapr1 libconfuse0 libxslt1.1 libconfuse-common ganglia-monitor-python; \
# dpkg -i hpccsystems-ganglia-monitoring--precise_*.deb; \

# Aliasing Apache web directory to use ganglia-webfrontend
echo "Alias /ganglia /usr/share/ganglia-webfrontend" >> /etc/apache2/apache2.conf; \
\
# Customizing names and labels
sed 's/my cluster\" localhost/VM Cluster\" localhost/g' < /etc/ganglia/gmetad.conf > /tmp/gmetad.conf; mv /tmp/gmetad.conf /etc/ganglia/gmetad.conf; \
echo "gridname \"HPCC\"" >> /etc/ganglia/gmetad.conf; \
\
# Setting up VM settings to get graphs up and running.  This overwrites many of the installed files.
cp -f ./header.tpl  /usr/share/ganglia-webfrontend/templates/default; \
cp -f ./host_view.tpl  /usr/share/ganglia-webfrontend/templates/default; \
cp -f ./cluster_view.tpl  /usr/share/ganglia-webfrontend/templates/default; \
\
cp -f ./conf.php /usr/share/ganglia-webfrontend/; \
cp -f ./get_context.php /usr/share/ganglia-webfrontend/; \
cp -f ./cluster_view.php /usr/share/ganglia-webfrontend/; \
\
cp -f ./query_count_report.php /usr/share/ganglia-webfrontend/graph.d; \
cp -f ./query_count_s_report.php /usr/share/ganglia-webfrontend/graph.d; \
cp -f ./roxie_instances_report.php /usr/share/ganglia-webfrontend/graph.d; \
\
mkdir /etc/ganglia/conf.d; \
cp -f ./modpython.conf /etc/ganglia/conf.d; \
cp -f ./gmond.conf /etc/ganglia; \
\
cp -f ./hpcc_logo.png /usr/share/ganglia-webfrontend/templates/default/images/; \
\
\
# Set gmond to start on reboot
cp ./gmond-start.conf /etc/init/; \
\
service gmetad stop; \
service ganglia-monitor stop
apachectl -k stop; \
sleep 5; \
\
rm -rf /var/lib/ganglia/rrds/*; \
\
service gmetad restart; \
service ganglia-monitor start
apachectl -k restart; \
echo "Done."
