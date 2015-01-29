#ifndef _DEFAULT_SETTINGS_HPP_
#define _DEFAULT_SETTINGS_HPP_

#define DEFAULT_ARR_SIZE    512

static const char *pDefaultRRDGraphPath("/usr/bin/rrdtool graph");
static const char *pDefaultRRDInfoPath("/usr/bin/rrdtool info");
static const char *pDefaultPathRRDRoot("/var/lib/ganglia/rrds/");
static const char *pSummaryInfo("__SummaryInfo__");
static const char *pDefaultPathSummaryInfo("/var/lib/ganglia/rrds/__SummaryInfo__/");
static const char *pRootFileName("tmpgraph");
static char pDestinationPath[DEFAULT_ARR_SIZE] = "/tmp/hpcc_ws_rrd_graphsXXXXXX";
static const char *pTempFileTemplate = "graphXXXXXX";
static const char *pFileTypeSVG("-a SVG");
static const char *pFileTypePNG("-a PNG");
static const char *pStartTime("--start");
static const char *pEndTime("--end");
static const char *pDataDefinitionPrefix1("DEF:ds");
static const char *pDataDefinitionSuffix(":sum:AVERAGE");
static const char *pLineDefinition("LINE");
static const char *pWidth("-w");
static const char *pHeight("-h");

#endif // _DEFAULT_SETTINGS_HPP_
