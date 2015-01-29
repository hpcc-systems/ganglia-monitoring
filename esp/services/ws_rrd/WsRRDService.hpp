#ifndef _ESPWIZ_WsRRD_HPP_
#define _ESPWIZ_WsRRD_HPP_

#include "ws_rrd_esp.ipp"

class Cws_rrdEx : public Cws_rrd
{
public:
  IMPLEMENT_IINTERFACE

  Cws_rrdEx();
  virtual ~Cws_rrdEx();
  virtual bool ongetGraphSVG(IEspContext &context, IEspGraphSVGDataRequest &req, IEspGraphSVGDataResponse &resp);
  virtual bool ongetAvailableMetrics(IEspContext &context, IEspGetAvailableMetricsRequest &req, IEspGetAvailableMetricsResponse &resp);
  virtual bool ongetAvailableServers(IEspContext &context, IEspGetAvailableServersForMetricsRequest &req, IEspGetAvailableServersForMetricsResponse &resp);
  virtual bool ongetAvailableClusters(IEspContext &context, IEspGetAvailableClustersRequest &req, IEspGetAvailableClustersResponse &resp);
};

#endif // _ESPWIZ_WsRRD_HPP_
