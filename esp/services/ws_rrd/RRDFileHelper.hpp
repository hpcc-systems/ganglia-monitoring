#ifndef _RRD_FILE_HELPER_HPP_
#define _RRD_FILE_HELPER_HPP_

class StringArray;
class StringBuffer;

class CRRDFileHelper
{
public:

    static bool getRRDFileNameRoots(const char *pCluster, const char *pServer, StringArray &arrFileNames);
    static bool getRRDServerDirectoryNames(const char *pCluster, StringArray &arrDirectoryNames);
    static bool getRRDFilePath(const char *pCluster, const char *pServer, StringBuffer &strPath);
};

#endif // _RRD_FILE_HELPER_HPP_
