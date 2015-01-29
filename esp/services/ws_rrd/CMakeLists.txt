################################################################################
#    HPCC SYSTEMS software Copyright (C) 2012 HPCC Systems.
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


# Component: ws_rrd
#####################################################
# Description:
# ------------
#    Cmake Input File for ws_rrd
#####################################################

project( ws_rrd )

include(${HPCC_GM_SOURCE_DIR}/esp/scm/additional.cmake)

set (    SRCS
         ${HPCC_GM_SOURCE_DIR}/esp/scm/ws_rrd.ecm
         ${ESPSCM_GENERATED_DIR}/ws_rrd_esp.cpp
         ./WsRRDService.cpp
         ./WsRRDPlugin.cpp
         ./RRDFileHelper.cpp
         ./RRDGraphWrapper.cpp
    )

include_directories (
         ${HPCC_SOURCE_DIR}/esp/esplib
         ${HPCC_SOURCE_DIR}/esp/platform
         ${HPCC_SOURCE_DIR}/system/jlib
         ${HPCC_SOURCE_DIR}/common/environment
         ${HPCC_SOURCE_DIR}/esp/services
         ${HPCC_SOURCE_DIR}/common
         ${HPCC_SOURCE_DIR}/system/security/securesocket
         ${HPCC_SOURCE_DIR}/system/security/shared
         ${HPCC_SOURCE_DIR}/system/include
         ${HPCC_SOURCE_DIR}/common/remote
         ${HPCC_SOURCE_DIR}/clients
         ${HPCC_SOURCE_DIR}/dali/base
         ${HPCC_SOURCE_DIR}/common/dllserver
         ${HPCC_SOURCE_DIR}/esp/bindings
         ${HPCC_SOURCE_DIR}/esp/bindings/SOAP/xpp
         ${HPCC_SOURCE_DIR}/esp/bindings/http/client
         ${HPCC_SOURCE_DIR}/esp/http/platform
         ${HPCC_SOURCE_DIR}/system/mp
         ${HPCC_SOURCE_DIR}/system/xmllib
         ${CMAKE_BINARY_DIR}
         ${CMAKE_BINARY_DIR}/oss
         ${CMAKE_BINARY_DIR}/esp/services/ws_rrd
    )

ADD_DEFINITIONS( -D_USRDLL )

HPCC_ADD_LIBRARY( ws_rrd SHARED ${SRCS}  )
add_dependencies (ws_rrd ws_rrdespscm)
install ( TARGETS ws_rrd RUNTIME DESTINATION ${EXEC_DIR} LIBRARY DESTINATION ${LIB_DIR} )
target_link_libraries ( ws_rrd
         jlib
         xmllib
         esphttp
         dalibase
         environment
         dllserver
         securesocket
    )
