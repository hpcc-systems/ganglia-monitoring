#include <cstdio>
#include "jstream.ipp"
#include "jfile.hpp"
#include "jprop.hpp"
#include "jlog.hpp"
#include "jhash.ipp"
#include <cstring>
#include "RRDGraphWrapper.hpp"
#include "RRDFileHelper.hpp"

// sample command line: rrdtool graph ~/tmp/out.svg -a SVG --end 1390817521  --start 1389125733  DEF:ds0a=./queryCount.rrd:sum:AVERAGE LINE1:ds0a#0000FF:"queryCount" -w 100 -h 100 -t "title"

static const char *PlotColor[] = { "0000FF", "FF0000", "00FF00", "008000", "800080", "808080", "FFFF00", "CC00FF", "CC99FF", "66FFCC",  "000000"};
static const int nPlotColors = 11;

typedef MapStringTo<StringBuffer, StringBuffer&> MapStrToStr;

void CRRDGraphWrapper::getUniqueID(const char *pID, StringBuffer &strNewID)
{
    static unsigned long long graphCount = 0;

    StringBuffer strID;

    strID.set(pID);

    strID.append("_hpcc-").append(graphCount);
    graphCount++;

    strNewID.clear().set(strID.str());
}

MemoryBuffer* CRRDGraphWrapper::getGraph(MemoryBuffer *pBuffer, const StringArray &strArrRRDFiles, const StringArray &strArrClusters, const StringArray &strArrServers,
                                            const long nStartTime, const long nEndTime, const int nWidth, const int nHeight, const char* pTitle,  const bool bGenPNG, const char* pRRDGraphPath)
{
    static CRRDGraphWrapper::CUniquePath UniquePath;

    if (pBuffer == NULL || nEndTime <= nStartTime || nHeight <= 0)
    {
        return NULL;
    }

    StringBuffer strRRDFilePath;
    StringBuffer strRRDGraphCmd(pRRDGraphPath == NULL ? pDefaultRRDGraphPath : pRRDGraphPath);

    StringBuffer strDestinationPath;
    UniquePath.getTempPath(strDestinationPath);

    strRRDGraphCmd.appendf(" %s", strDestinationPath.str());
    strRRDGraphCmd.appendf(" %s", bGenPNG == false ? pFileTypeSVG : pFileTypePNG);
    strRRDGraphCmd.appendf(" %s %ld", pStartTime, nStartTime);
    strRRDGraphCmd.appendf(" %s %ld", pEndTime, nEndTime);

    int nClusterCount = strArrClusters.length();
    int nServerCount = strArrServers.length();
    int nRRDFileCount = strArrRRDFiles.length();
    int nLineCount = 1;

    bool bClusterSpecified = true;
    if (nClusterCount == 0)
    {
         bClusterSpecified = false;
    }
    bool bServerSpecified = true;
    if (nServerCount == 0)
    {
         bServerSpecified = false;
    }

    if (bServerSpecified == true && bClusterSpecified == false) // invalid
    {
        PROGLOG("ganglia-monitoring: Cannot specifiy server with no cluster");
        throw MakeStringException(0, "ganglia-monitoring: Cannot specifiy server with no cluster");
    }

    for (int idxMetric = 0; idxMetric < nRRDFileCount; idxMetric++)
    {
        for (int idx = 0; (idx < nClusterCount || bClusterSpecified == false) && (idx < nServerCount || bServerSpecified == false) && idxMetric < nRRDFileCount && idx < nPlotColors; idx++)
        {
            const char *pServer = bServerSpecified ? strArrServers.item(idx) : "";
            const char *pCluster = bClusterSpecified ? strArrClusters.item(idx) : "";
            const char *pRRDFile = strArrRRDFiles.item(idxMetric);

            if ((pServer == NULL || strcmp(pServer, pSummaryInfo) == 0 || pServer[0] == 0) && (pCluster == NULL || *pCluster == 0))
            {
                strRRDFilePath.set(pDefaultPathSummaryInfo);
            }
            else
            {
                strRRDFilePath.set(pDefaultPathRRDRoot);
                strRRDFilePath.appendf("%s/", pCluster);

                if (pServer != NULL && *pServer != 0)
                {
                    strRRDFilePath.append(pServer);
                }
                else
                {
                    strRRDFilePath.append(pSummaryInfo);
                }
                strRRDFilePath.append("/");
            }
            strRRDFilePath.appendf("%s.rrd", pRRDFile);

            if (checkFileExists(strRRDFilePath.str()) == false)
            {
                PROGLOG("Can not find rrd file for '%s'", strRRDFilePath.str());
                throw MakeStringException(0, "Can not find rrd file for '%s'", strRRDFilePath.str());
            }

            strRRDGraphCmd.appendf(" %s%d%d=%s", pDataDefinitionPrefix1, idxMetric+1, idx+1, strRRDFilePath.str());
            strRRDGraphCmd.appendf("%s", pDataDefinitionSuffix);
            strRRDGraphCmd.appendf(" %s%d:ds%d%d#%s:%s", pLineDefinition, nLineCount++, idxMetric+1, idx+1, PlotColor[(nLineCount-1)%nPlotColors], pRRDFile);

            if (bServerSpecified == false || bClusterSpecified == false)
            {
                break;
            }
        }
    }

    strRRDGraphCmd.appendf(" %s %d", pWidth, nWidth);
    strRRDGraphCmd.appendf(" %s %d", pHeight, nHeight);

    if (pTitle != NULL && *pTitle != 0)
    {
        strRRDGraphCmd.appendf(" -t '%s'", pTitle);
    }

    PROGLOG("RRDTOOL GRAPH CMD --> %s <--", strRRDGraphCmd.str());
    FILE *fp = popen(strRRDGraphCmd.str(), "r");

    if (fp == NULL)
    {
        return NULL;
    }

    pclose(fp);

    fp = fopen(strDestinationPath.str(),"r");

    if (fp == 0)
    {
        return NULL;
    }

    CFileInputStream svgFileIStream(fileno(fp));

    int nCharacter = -1;

    pBuffer->clear();

    StringBuffer strBufferIn;

    char removedChars[64] = {0};

    int nCount = 0;
    do
    {
        nCharacter = svgFileIStream.readNext();

        if (nCharacter != -1 && (nCount > 37 || bGenPNG == true))  // remove xml tag in svg
        {
            strBufferIn.append(static_cast<unsigned char>(nCharacter));
        }
        else if (nCharacter != -1)
        {
            removedChars[nCount] = nCharacter;
        }
        nCount++;
    }
    while(nCharacter != -1);

    if (*removedChars != 0)
    {
        DBGLOG("Removing XML tag:%s", removedChars);
    }

    StringBuffer strBufferIn2(strBufferIn.str());
    strBufferIn.clear().set(strBufferIn2.str());

    fclose(fp);

    const int nOffSet = 4;
    char originalID[1024] = "";
    char *pBufferIn = new char[strBufferIn.length()+1];
    strncpy(pBufferIn, strBufferIn.str(), strBufferIn.length()+1);

    char *pStart = NULL;
    char *pEnd = NULL;

    pStart = strstr(const_cast<char*>(pBufferIn), "id=\"");
    pEnd = strstr(pStart+nOffSet, "\"");

    while (pStart != NULL)
    {
        int len = pEnd-pStart-nOffSet;

        if (len > 1024)
        {
	    delete[] pBufferIn;
            PROGLOG("SVG id too long");
            return NULL;
        }

        strncpy(originalID, pStart+nOffSet, len);
        originalID[len] = 0;

        StringBuffer strNewID;
        getUniqueID(originalID, strNewID);

        StringBuffer strOriginalIdWithQuote("\"");
        strOriginalIdWithQuote.append(originalID).append("\"");

        StringBuffer strNewIDWithQuote("\"");
        strNewIDWithQuote.append(strNewID.str()).append("\"");

        strBufferIn2.clear().set(strBufferIn.str());
        strBufferIn.clear().set(strBufferIn2.str());

        strBufferIn.replaceString(strOriginalIdWithQuote.str(), strNewIDWithQuote.str());

        StringBuffer strOriginalIdWithHashTag("\"#");
        strOriginalIdWithHashTag.append(originalID).append("\"");

        StringBuffer strNewIDWithHashTag("\"#");
        strNewIDWithHashTag.append(strNewID.str()).append("\"");

        strBufferIn.replaceString(strOriginalIdWithHashTag.str(), strNewIDWithHashTag.str());

        StringBuffer strOriginalIdWithParen("(#");
        strOriginalIdWithParen.append(originalID).append(")");

        StringBuffer strNewIDWithParen("(#");
        strNewIDWithParen.append(strNewID.str()).append(")");

        StringBuffer strMM(strBufferIn.str());
        strMM.replaceString(strOriginalIdWithParen.str(), strNewIDWithParen.str());
        strBufferIn.set(strMM.str());

        pStart = strstr(pEnd, "id=\"");

        if (pStart == NULL)
        {
            break;
        }
        pEnd = strstr(pStart+nOffSet, "\"");
    }

    pBuffer->resetBuffer();
    pBuffer->append(strBufferIn.str());
    delete[] pBufferIn;

    DeleteFile(strDestinationPath.str());

    return pBuffer;
}

CRRDGraphWrapper::CUniquePath::CUniquePath() : m_strTempDirectory(mkdtemp(pDestinationPath))
{
    int nRetVal =_mkdir(m_strTempDirectory.str());

    PROGLOG("creating temp dir: %s", m_strTempDirectory.str());

    if (nRetVal != 0)
    {
        ERRLOG("_mkdir failed with errno = %d", errno);
    }
}

CRRDGraphWrapper::CUniquePath::~CUniquePath()
{
    rmdir(m_strTempDirectory.str());
}

void CRRDGraphWrapper::CUniquePath::getTempPath(StringBuffer &strUniqueName)
{
    strUniqueName.setf("%s%c%s", m_strTempDirectory.str(), PATHSEPCHAR, pTempFileTemplate);

    char *pTempFilePath = new char[strUniqueName.length()+1];
    strcpy(pTempFilePath, strUniqueName.str());

    close(mkstemp(pTempFilePath));

    strUniqueName.set(pTempFilePath);
}
