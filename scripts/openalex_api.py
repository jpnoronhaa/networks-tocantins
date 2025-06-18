from pyalex import Authors, config

config.email = "pedro.noronha@uft.edu.br"

fields = [
  'id',
  'display_name',
  'ids',
  'last_known_institutions',
  'summary_stats',
  'works_count',
  'summary_stats',
  'works_count'
]

all_authors = []

pager = Authors().filter(openalex="https://openalex.org/A5054472989|https://openalex.org/A5034079036").select(fields).paginate(method="page", per_page=200)

for page in pager:
  all_authors.extend(page)

print(all_authors)
print(type(all_authors[0]))
