import argparse
import rdt_2_1 as RDT

if __name__ == '__main__':
    parser =  argparse.ArgumentParser(description='Pig Latin conversion server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()

    rdt = RDT.RDT('server', None, args.port)
    rdt.disconnect()
