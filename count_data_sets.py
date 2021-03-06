import re
from flashtext import KeywordProcessor


keyword_processor = KeywordProcessor(case_sensitive=True)
data_set_count = {}
with open("dataset-names-clean.txt", "r") as inp:
    for line in inp:
        data_set_name = line.strip().strip("'").strip('"')
        data_set_name_cleaned = re.sub(r"[\(\)]", "", data_set_name).strip()
        data_set_count[data_set_name_cleaned] = 0
        keyword_processor.add_keyword(data_set_name_cleaned)

line_count = 1
citation_context_count = data_set_count.copy()
with open("/vol3/erhan/he9318-mag-20191226-0/nlp/PaperCitationContexts.txt", "r") as inp:
    with open("citation_context_matches_CS.txt", "w") as outp:
        for line in inp:
            paper_id, reference_id, citation_context = line.strip("\n").split("\t")
            keywords_found = keyword_processor.extract_keywords(citation_context, span_info=True)
            if keywords_found:
                for keyword in keywords_found:
                    citation_context_count[keyword[0]] += 1
                    outp.write("\t".join(map(str, keyword)) + "\t" +  "\t".join([paper_id, reference_id, citation_context]) + "\n")
            line_count += 1
with open("citation_context_count_CS.txt", "w") as outp:
    for item in citation_context_count:
        outp.write(str(item) + "\t" + str(citation_context_count[item]) + "\n")

line_count = 1
abstract_count = data_set_count.copy()
with open("/vol3/erhan/he9318-mag-20191226-0/PaperAbstracts_CS_nonPatent.txt", "r") as inp:
    with open("abstract_matches_CS.txt", "w") as outp:
            for line in inp:
                paper_id, abstract = line.strip("\n").split("\t")
                keywords_found = keyword_processor.extract_keywords(abstract, span_info=True)
                if keywords_found:
                    for keyword in keywords_found:
                        abstract_count[keyword[0]] += 1
                        outp.write("\t".join(map(str, keyword)) + "\t" + "\t".join([paper_id, abstract]) + "\n")
                line_count += 1
with open("abstract_count_CS.txt", "w") as outp:
    for item in abstract_count:
        outp.write(str(item) + "\t" + str(abstract_count[item]) + "\n")
