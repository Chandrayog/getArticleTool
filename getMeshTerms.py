from pubmed_lookup import PubMedLookup
from pubmed_lookup import Publication
import json
import os

# NCBI will contact user by email if excessive queries are detected
email = ''


# url1 = 'http://www.ncbi.nlm.nih.gov/pubmed/22331878'
# url2=  'https://pubmed.ncbi.nlm.nih.gov/26667886/'


def getMeshIDs(data, email):

    meshTerms = []
    article_ids = parseUrlforIDs(data)
    for id in article_ids:
        url = 'http://www.ncbi.nlm.nih.gov/pubmed/' + id
        lookup = PubMedLookup(url, email)

        #call the pubmed library to look for the article data
        publication = Publication(lookup)    # Use 'resolve_doi=False' to keep DOI URL
        xmlDict=publication.get_pubmed_xml()

        #object to hold all terms


        #parse the xml dictionary and get the data
        for meshcode in xmlDict['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['MeshHeadingList']['MeshHeading']:
               meshTerms.append(meshcode['DescriptorName']['#text'])


    saveOutput(meshTerms)
        #return meshTerms
        #print(meshTerms)


def parseUrlforIDs(data):

    articelID=[]
    for i in range(len(data)):
        for item in data[i]['entities']['items']:
            articelID.append(str(item['URLs']).split('gov',1)[1].replace('/',''))

    return articelID

def saveOutput(data):
    try:

        if os.path.exists("MeshTerms.txt"):
           os.remove("MeshTerms.txt")
           with open("MeshTerms.txt", "x") as fp:
               fp.write("\n".join(str(item) for item in data))
               print('Data Saved')
        else:
            with open("MeshTerms.txt", "x") as fp:
                fp.write("\n".join(str(item) for item in data))
                print('Data Saved')
    except Exception as e:  # raise e
           pass
           print("Exception Occurred :", e)

