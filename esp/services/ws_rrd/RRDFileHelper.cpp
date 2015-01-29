#include "jfile.hpp"
#include "jstring.hpp"
#include "DefaultRRDSettings.hpp"
#include "RRDFileHelper.hpp"

bool CRRDFileHelper::getRRDFileNameRoots(const char *pCluster, const char *pServer, StringArray &arrFileNames)
{
    StringBuffer strPath;

    if (CRRDFileHelper::getRRDFilePath(pCluster, pServer, strPath) == false)
    {
        return false;
    }
    Owned<IFile> summaryInfoDir = createIFile(strPath.str());
    const char *pMask = "*.rrd";

    Owned<IDirectoryIterator> rrdFiles = summaryInfoDir->directoryFiles(pMask, false, false);

    ForEach(*rrdFiles)
    {
        StringBuffer strRRDMetric(&rrdFiles->query().queryFilename()[strPath.length()]);
        strRRDMetric.setLength(strRRDMetric.length()-4);  // trim .rrd
        arrFileNames.append(strRRDMetric.str());
    }

    return true;
}

bool CRRDFileHelper::getRRDServerDirectoryNames(const char *pCluster, StringArray &arrDirectoryNames)
{
    StringBuffer strPath(pDefaultPathRRDRoot);

    if (pCluster != NULL && *pCluster != 0 && strcmp(pCluster, pSummaryInfo) != 0)
    {
        strPath.appendf("%c%s%c", PATHSEPCHAR, pCluster, PATHSEPCHAR);
    }

    Owned<IFile> summaryInfoDir = createIFile(strPath.str());

    if (checkFileExists(strPath.str()) == false)
    {
        return false;
    }

    const char *pMask = "*";

    Owned<IDirectoryIterator> directories = summaryInfoDir->directoryFiles(pMask, false, true);

    ForEach(*directories)
    {
        if (strcmp(&(directories->query().queryFilename()[strPath.length()]), pSummaryInfo) != 0)
        {
            arrDirectoryNames.append(&(directories->query().queryFilename()[strPath.length()]));
        }
    }

    return true;
}

bool CRRDFileHelper::getRRDFilePath(const char *pCluster, const char *pServer, StringBuffer &strPath)
{
    strPath.set(pDefaultPathRRDRoot);

    if ((pCluster == NULL || *pCluster == 0) && (pServer == NULL || *pServer == 0))
    {
        strPath.appendf("/%s/", pSummaryInfo);
    }
    else if (pCluster != NULL && *pCluster != 0 && (pServer == NULL || *pServer == 0) && strcmp(pCluster, pSummaryInfo) != 0)
    {
        strPath.appendf("/%s/%s/", pCluster, pSummaryInfo);
    }
    else if (pCluster != NULL && *pCluster != 0 && pServer != NULL && *pServer != 0 && strcmp(pServer, pSummaryInfo))
    {
        strPath.appendf("/%s/%s/", pCluster, pServer);
    }

    if (checkFileExists(strPath.str()) == false)
    {
        strPath.clear();

        return false;
    }

    return true;
}
