from datetime import datetime
from file_finder.exceptions import InvalidInputError


def get_folders(path):
    """
   Obtém todos os arquivos no diretório pesquisado
   :param path: um objeto Path() que representa o diretório
   :return: uma lista de objetos Path() em que cada elemento será um arquivo que existe em `path`
   """
    return [item for item in path.iterdir() if item.is_dir()]

def get_files(path):
    """
    Obtém todos os arquivos no diretório pesquisado
    :param path: um objeto Path() que representa o diretório
    :return: uma lista de objetos Path() em que cada elemento será um arquivo que existe em `path`
    """
    return [ item for item in path.iterdir() if item.is_file()]

def find_by_name(path, value):
    """
        Verifica se o arquivo com o nome escolhido existe
        :param path: um objeto Path() que representa o diretório
        :param value: uma string com o nome do arquivo pesquisado
        :return: uma lista de objetos Path() em que cada elemento será um arquivo que existe em `path`
        """
    return [file for file in get_files(path) if file.stem == value]

def find_by_ext(path, value):
    """
            Verifica se os arquivso com a extensão escolhida existe
            :param path: um objeto Path() que representa o diretório
            :param value: uma string com a extensão pesquisada
            :return: uma lista de objetos Path() em que cada elemento será um arquivo que existe em `path`
            """
    return [file for file in get_files(path) if file.suffix == value]

def find_by_mod(path, value):
    #input: dd/mm/aaaa
    try:
        datetime_obj = datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise InvalidInputError(f"'{value}' is not a valid date in format: dd/mm/aaaa.")

    return [file for file in get_files(path) if datetime.fromtimestamp(file.stat().st_mtime) >= datetime_obj]




    pass

def timestamp_to_string(timestamp):
    datetime_obj = datetime.fromtimestamp(timestamp)
    return datetime_obj.strftime("%d/%m/%Y - %H:%M:%S:%f")

def get_files_details(files):
    files_details = []
    for file in files:
        detailes = [
            file.name,
            file.suffix,
            timestamp_to_string(file.stat().st_mtime),
            file.parent.absolute()
        ]
        files_details.append(detailes)

    return files_details