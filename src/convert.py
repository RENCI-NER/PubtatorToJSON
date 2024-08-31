import argparse
import json

from pubtator_loader import PubTatorCorpusReader
from utils import normalize_nodes


def convert(infile, outfile):
    data_reader = PubTatorCorpusReader(infile)
    corpus = data_reader.load_corpus() # corpus is a List[PubtatorDocuments]
    results = [{
        'text': f"{doc.title_text} {doc.abstract_text}",
        'pmid': doc.id,
        'entities': [{
            'start_index': ent.start_index,
            'end_index': ent.end_index,
            'text_segment': ent.text_segment,
            'identifier': f'UMLS:{ent.entity_id}'
            } for ent in doc.entities
        ]} for doc in corpus
    ]
    entities = [res['identifier'] for result in results for res in result['entities']]
    unique_entity_ids = list(set(entities))
    print(f'unique entity ids len: {len(unique_entity_ids)}')
    norm_results = normalize_nodes(unique_entity_ids)
    print(f'norm results len: {len(norm_results)}')
    for res in results:
        for ent in res['entities']:
            if norm_results[ent['identifier']]:
                ent['equivalent_identifiers'] = norm_results[ent['identifier']]['equivalent_identifiers']
                ent['biolink_types'] = norm_results[ent['identifier']]['type']
            else:
                ent['equivalent_identifiers'] = None
                ent['biolink_types'] = None

    with open(outfile, 'w') as out_f:
        json.dump(results, out_f, indent=2)

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input/output arguments.')
    parser.add_argument('--input_file', type=str,
                        default='/home/hongyi/MedMentions/full/data/corpus_pubtator.txt',
                        help='input file in pubtator format')
    parser.add_argument('--output_file', type=str,
                        default='/home/hongyi/MedMentions/full/data/corpus_pubtator.json',
                        help='output file that contains converted file from input_file in JSON with entity ID '
                             'normalized using RENCI nodenorm service')

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    convert(input_file, output_file)
    exit(0)
