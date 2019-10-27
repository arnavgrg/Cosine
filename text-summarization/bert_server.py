from bert_serving.server.helper import get_args_parser
from bert_serving.server import BertServer

def main():
    args = get_args_parser().parse_args(['-model_dir', './uncased_L-12_H-768_A-12',
                                     '-port', '5555',
                                     '-port_out', '5556',
                                     '-max_seq_len', '25',
                                     '-num_worker', '1',
                                     '-mask_cls_sep',
                                     '-cpu'])
    server = BertServer(args)
    server.start()

if __name__ == "__main__":
    main()