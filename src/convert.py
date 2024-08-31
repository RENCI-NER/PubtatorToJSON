import argparse
from pubtator_loader import PubTatorCorpusReader
from utils import normalize_nodes


def convert(infile, outfile):
    results = []
    data_reader = PubTatorCorpusReader(infile)
    corpus = data_reader.load_corpus() # corpus is a List[PubtatorDocuments]
    for doc in corpus:
        results.append({
            'text': f"{doc.title_text} {doc.abstract_text}",
            'pmid': doc.id,
            'entities': [{'start_index': ent.start_index,
                          'end_index': ent.end_index,
                          'text_segment': ent.text_segment,
                          'entity_id': ent.entity_id
                          }
                         for ent in doc.entities]
        })

    entities = [res['entity_id'] for result in results for res in result['entities']]
    unique_entity_ids = list(set(entities))
    print(f'unique_entity_ids: {unique_entity_ids}')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input/output arguments.')
    parser.add_argument('--input_file', type=str,
                        default='/home/hongyi/MedMentions/full/data/corpus_pubtator_cut.txt',
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
