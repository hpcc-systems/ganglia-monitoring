################################################################################
#    HPCC SYSTEMS software Copyright (C) 2014 HPCC Systems.
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

INSTALL( FILES ${CMAKE_CURRENT_SOURCE_DIR}/ganglia.js DESTINATION componentfiles/files/ganglia/nls COMPONENT Runtime )
INSTALL( FILES ${CMAKE_CURRENT_SOURCE_DIR}/es/ganglia.js DESTINATION componentfiles/files/ganglia/nls/es COMPONENT Runtime )
INSTALL( FILES ${CMAKE_CURRENT_SOURCE_DIR}/bs/ganglia.js DESTINATION componentfiles/files/ganglia/nls/bs COMPONENT Runtime )
INSTALL( FILES ${CMAKE_CURRENT_SOURCE_DIR}/hr/ganglia.js DESTINATION componentfiles/files/ganglia/nls/hr COMPONENT Runtime )
INSTALL( FILES ${CMAKE_CURRENT_SOURCE_DIR}/hu/ganglia.js DESTINATION componentfiles/files/ganglia/nls/hu COMPONENT Runtime )
INSTALL( FILES ${CMAKE_CURRENT_SOURCE_DIR}/pt-br/ganglia.js DESTINATION componentfiles/files/ganglia/nls/pt-br COMPONENT Runtime )
INSTALL( FILES ${CMAKE_CURRENT_SOURCE_DIR}/sr/ganglia.js DESTINATION componentfiles/files/ganglia/nls/sr COMPONENT Runtime )
INSTALL( FILES ${CMAKE_CURRENT_SOURCE_DIR}/zh/ganglia.js DESTINATION componentfiles/files/ganglia/nls/zh COMPONENT Runtime )

