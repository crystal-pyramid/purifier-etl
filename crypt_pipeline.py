import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from binance.client import Client

import argparse
import os

import src.binanceapi_util as bu

parser = argparse.ArgumentParser(description='Pipeline for getting BTC Price')
parser.add_argument('--bucket', required=True, help='Specify Cloud Storage bucket for output')
parser.add_argument('--project',required=True, help='Specify Google Cloud project')
parser.add_argument('--region',required=False, help='Specify Google Cloud region',default="asia-northeast1")
parser.add_argument('--worker_machine_type',required=False,help='Specify Type of workers',default="e2-standard-2")
parser.add_argument('--max_num_workers',required=False,help='Specify Maximum Number of workers',default=4)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--DirectRunner',action='store_true')
group.add_argument('--DataFlowRunner',action='store_true')

opts = parser.parse_args()

if opts.DirectRunner:
    runner='DirectRunner'
if opts.DataFlowRunner:
    runner='DataFlowRunner'

bucket = opts.bucket
project = opts.project
region = opts.region
worker_machine_type = opts.worker_machine_type
max_num_workers = opts.max_num_workers

argv = [
    '--project={0}'.format(project),
    '--region={0}'.format(region),
    '--save_main_session',
    '--runner={0}'.format(runner),
    '--worker_machine_type={0}'.format(worker_machine_type),
    '--staging_location=gs://{0}/staging/'.format(bucket),
    '--temp_location=gs://{0}/staging/'.format(bucket),
    '--runner={0}'.format(runner),
    '--max_num_workers={0}'.format(max_num_workers),
    '--requirements_file requirements.txt'
    ]


def run():

    # パイプラインの定義
    p = beam.Pipeline(argv=argv)
    # Binanceクライアントの初期化
    client = bu.initialize_binance_client()

    execute_api = ( p 
    | 'Create' >> beam.Create([None])
    | 'Get BTC Price' >> beam.Map(bu.get_btc_price, client=client))

    output_local = ( execute_api 
    | "Convert to JSON" >> beam.Map(bu.to_json)
    | "Write to File" >> beam.io.WriteToText('./data/crypt_price', file_name_suffix='.json'))
    
    
    print_price = execute_api |'Print' >> beam.Map(print)

    p.run()

if __name__ == "__main__":
    run()