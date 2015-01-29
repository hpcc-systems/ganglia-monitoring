#include "WsRRDService.hpp"
#include "RRDGraphWrapper.hpp"
#include "RRDFileHelper.hpp"

Cws_rrdEx::Cws_rrdEx()
{
}

Cws_rrdEx::~Cws_rrdEx()
{
}

bool Cws_rrdEx::ongetGraphSVG(IEspContext &context, IEspGraphSVGDataRequest &req, IEspGraphSVGDataResponse &resp)
{
    MemoryBuffer GraphBuffer;

    CRRDGraphWrapper::getGraph(&GraphBuffer, req.getRRDMetrics(), req.getClusters(), req.getServers(), req.getStartTime(), req.getEndTime(),
                                    req.getWidth(), req.getHeight(), req.getTitle(), false);

    resp.setGraph(GraphBuffer.toByteArray());

    return true;
}

bool Cws_rrdEx::ongetAvailableMetrics(IEspContext &context, IEspGetAvailableMetricsRequest &req, IEspGetAvailableMetricsResponse &resp)
{
    StringArray arrRRDMetrics;

    CRRDFileHelper::getRRDFileNameRoots(req.getCluster(), req.getServer(), arrRRDMetrics);

    resp.setMetrics(arrRRDMetrics);

    return true;
}

bool Cws_rrdEx::ongetAvailableServers(IEspContext &context, IEspGetAvailableServersForMetricsRequest &req, IEspGetAvailableServersForMetricsResponse &resp)
{
    StringArray arrRRDServers;

    if (strlen(req.getCluster()) > 0)
    {
        CRRDFileHelper::getRRDServerDirectoryNames(req.getCluster(), arrRRDServers);

        resp.setServers(arrRRDServers);
    }

    return true;
}

bool Cws_rrdEx::ongetAvailableClusters(IEspContext &context, IEspGetAvailableClustersRequest &req, IEspGetAvailableClustersResponse &resp)
{
    StringArray arrRRDClusters;

    CRRDFileHelper::getRRDServerDirectoryNames(NULL, arrRRDClusters);

    resp.setClusters(arrRRDClusters);

    return true;
}
