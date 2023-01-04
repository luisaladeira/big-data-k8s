from __future__ import annotations

import os
import json
import logging

import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd

from io import BytesIO

from azure.storage.filedatalake import DataLakeServiceClient, FileSystemClient


class Datalake:
    """ Classe para upload, download e listagem de arquivos em um Azure Datalake. """

    def __init__(self, account_name: str, account_key: str):
        self.account_name = account_name
        self.account_key = account_key

        try:
            self.service = DataLakeServiceClient(
                account_url=f'https://{self.account_name}.dfs.core.windows.net',
                credential=self.account_key
            )
        except ConnectionError as err:
            logging.error(f'Erro de conexão com Datalake. {err}')

    def create_file_system(self, file_system_name: str) -> FileSystemClient:
        """ Cria um FileSystem com o nome especificado. """

        file_system_client = None

        try:
            file_system_client = self.service.create_file_system(
                file_system=file_system_name)
        except Exception:
            file_system_client = self.service.get_file_system_client(
                file_system_name)
        except Exception:
            file_system_client = self.service.get_file_system_client(
                file_system_name)
        else:
            logging.error(
                f'Erro na criação do file system {file_system_name}.')
        finally:
            return file_system_client

    def create_directory(self, file_system_client: FileSystemClient, directory_name: str):
        """ Cria um diretório no Datalake. """

        try:
            file_system_client.create_directory(directory_name)
        except Exception as err:
            logging.error(
                f'Erro na criação do diretório {directory_name}. {err}')

    def upload_file_to_directory(self, file_system_name: str,
                                 directory_name: str, file_name_dest: str,
                                 content: pd.DataFrame = None, file_name_orig: str = None):
        """ Faz o upload de um arquivo local ou list/dict/Dataframe ao Datalake. """

        if file_name_orig and not os.path.isfile(file_name_orig):
            logging.error(
                f'Arquivo {file_name_orig} não encontrado localmente.')
            return

        try:
            file_system_client = self.service.get_file_system_client(
                file_system=file_system_name)

            directory_client = file_system_client.get_directory_client(
                directory_name)

            file_client = directory_client.create_file(file_name_dest)

            if '.parquet' in file_name_dest:
                table = pa.Table.from_pandas(content)
                buffer = pa.BufferOutputStream()
                pq.write_table(table, buffer)
                data = buffer.getvalue().to_pybytes()
            else:
                data = json.dumps(content)

            file_client.append_data(data=data, offset=0, length=len(data))

            file_client.flush_data(len(data))

            logging.info(f'Arquivo {file_name_dest} upado com sucesso.')
        except Exception as err:
            logging.error(f'Erro no upload do arquivo {file_name_orig} '
                          f'para o diretório {directory_name} no Datalake. {err}')

    def upload_file_to_directory_bulk(self, file_system_name: str, directory_name: str,
                                      file_origin: str | bytes, file_name_dest: str):
        """ Faz o upload de um arquivo local ao datalake. """

        if type(file_origin) is str and not os.path.isfile(file_origin):
            print(f'Arquivo {file_origin} não encontrado localmente.')
            return False
        try:
            file_system_client = self.service.get_file_system_client(
                file_system=file_system_name)

            directory_client = file_system_client.get_directory_client(
                directory_name)

            file_client = directory_client.get_file_client(file_name_dest)

            if type(file_origin) is str:
                local_file = open(file_origin, 'rb')
            else:
                local_file = BytesIO(file_origin)

            file_contents = local_file.read()

            file_client.upload_data(file_contents, overwrite=True)

            logging.info(f'Arquivo {file_name_dest} upado com sucesso.')
        except Exception as err:
            logging.error(f'Erro no upload do arquivo {file_name_dest} '
                          f'para o diretório {directory_name} no Datalake. {err}')

    def list_directory_contents(self, file_system_name: str, directory_name: str) -> list:
        """ Lista o conteúdo de um diretório no Datalake. """

        try:
            file_system_client = self.service.get_file_system_client(
                file_system=file_system_name)

            paths = file_system_client.get_paths(path=directory_name)

            return [path.name for path in paths]
        except Exception as err:
            logging.error(
                f'Erro ao listar o conteúdo do diretório {directory_name}. {err}')
            return []

    def download_file_from_directory(self, file_system_name: str,
                                     directory_name: str, filename: str) -> BytesIO:
        """ Faz o download de um arquivo do Datalake. """

        local_file = BytesIO()

        try:
            file_system_client = self.service.get_file_system_client(
                file_system=file_system_name)

            directory_client = file_system_client.get_directory_client(
                directory_name)

            file_client = directory_client.get_file_client(filename)

            download = file_client.download_file()

            downloaded_bytes = download.readall()

            local_file.write(downloaded_bytes)

            local_file.seek(0)
        except Exception as err:
            logging.error('[Datalake] Não foi possivel fazer o download do item '
                          f'{directory_name}/{filename}. {err}')
        finally:
            return local_file