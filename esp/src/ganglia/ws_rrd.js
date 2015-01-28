/*##############################################################################
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
############################################################################## */
define([
    "dojo/_base/declare",
    "dojo/store/Observable",


    "hpcc/ESPRequest"
], function (declare, Observable,
    ESPRequest) {
    var GangliaMetricStore = declare([ESPRequest.Store], {
        service: "ws_rrd",
        action: "getAvailableMetrics",
        responseQualifier: "GetAvailableMetricsResponse.Metrics",
        idProperty: "Item",
    });

    var GangliaServerStore = declare([ESPRequest.Store], {
        service: "ws_rrd",
        action: "getAvailableServers",
        responseQualifier: "GetAvailableServersForMetricsResponse.Servers",
        idProperty: "Item",
    });

    return {
        GangliaClusterList: function (params) {
            return ESPRequest.send("ws_rrd", "getAvailableClusters", params);
        },

        GangliaServerList: function (params) {
            return ESPRequest.send("ws_rrd", "getAvailableServers", params);
        },

        GangliaMetricList: function (params) {
            return ESPRequest.send("ws_rrd", "getAvailableMetrics", params);
        },

        GangliaRRDGraphList: function (params) {
            return ESPRequest.send("ws_rrd", "getGraphSVG", params);
        },

        CreateGangliaServerStore: function (options) {
            var store = new GangliaServerStore(options);
            return Observable(store);
        },

        CreateGangliaMetricStore: function (options) {
            var store = new GangliaMetricStore(options);
            return Observable(store);
        }
    };
});
