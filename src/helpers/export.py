import pandas as pd
from edie.model import Metadata
from edie.api import ApiClient

def export_datframe():
    api = ApiClient(endpoint='http://lexonomy.elex.is/', api_key='GXCQJ6S2FZUATM5Z2S0MGZ7XOMXKUFNP')
    all_langs = {}

    all_dicts = api.dictionaries()
    print(all_dicts)

    for d in all_dicts['dictionaries']:

        try:
            metadata: Metadata = Metadata(api.about(dictionary_id=d))

            if metadata.title not in all_langs:
                if not metadata.source_language:
                    metadata.source_language=''
                all_langs[metadata.title] = {'title':metadata.title,
                                            'src_language':metadata.source_language,
                                             'trg_language':metadata.target_language,
                                             'genre':metadata.genre,
                                             'size': metadata.entryCount,
                                             'ids':[d]}
            else:
                all_langs[metadata.title]['ids'].append(d)
        except:
            print('issue with '+d)

    all_langs_sorted = sorted(all_langs.values(), key=lambda i: i['src_language'])
    df = pd.DataFrame(all_langs_sorted)
    df.to_csv('lex_data.csv')

export_datframe()