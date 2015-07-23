from Bio import Entrez # install with 'pip install biopython'
from Bio.Entrez import efetch, read
Entrez.email = "your@email.com" # register your email

def get_mesh(pmid):
    # call PubMed API
    handle = efetch(db='pubmed', id=str(pmid), retmode='xml')
    xml_data = read(handle)[0]
    # skip articles without MeSH terms
    if u'MeshHeadingList' in xml_data['MedlineCitation']:
        for mesh in xml_data['MedlineCitation'][u'MeshHeadingList']:
            # grab the qualifier major/minor flag, if any
            major = 'N'
            qualifiers = mesh[u'QualifierName']
            if len(qualifiers) > 0:
                major = str(qualifiers[0].attributes.items()[0][1])
            # grab descriptor name
            descr = mesh[u'DescriptorName']
            name = descr.title()

            yield(name, major)

# example output
for name, major in get_mesh(128):
    print '{}, {}'.format(name, major)
