################################################################################
#   HPCC SYSTEMS software Copyright (C) 2018 HPCC Systems.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
################################################################################
SET (GANGLIA_SOURCE_DIR "${HPCC_SOURCE_DIR}/esp/src/ganglia")

FOREACH( iFILES
        ${GANGLIA_SOURCE_DIR}/GangliaFilterDropDownWidget.js
        ${GANGLIA_SOURCE_DIR}/GangliaWidget.js
        ${GANGLIA_SOURCE_DIR}/ws_rrd.js
        ${GANGLIA_SOURCE_DIR}/ganglia.json
)

        INSTALL( FILES ${iFILES} DESTINATION componentfiles/files/ganglia COMPONENT Runtime )
ENDFOREACH( iFILES )
