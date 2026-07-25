import json, os
DATABASE_FOLDER = 'database'
get_filepath = lambda fn: os.path.join(DATABASE_FOLDER, f'{fn}.json')


def get_listname_list() -> list[str]:
    lst = os.listdir(DATABASE_FOLDER)
    return list(map(lambda x: x[:-5], lst))


def destroy_list(listname: str) -> bool:
    fp = get_filepath(listname)
    exists = os.path.exists(fp)

    if exists: os.remove(fp)
    return exists


def load(filename: str) -> list[str]:
    filepath = get_filepath(filename)

    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r') as f:
        return json.load(f)


def save(filename: str, lst: list[str]):
    with open(get_filepath(filename), 'w') as f:
        json.dump(lst, f)


class ListRecorder:
    def __init__(self, listname: str):
        self.__listname = listname
        self.__content = load(listname)

    def get_content(self) -> list[str]:
        return self.__content.copy()

    def change_listsave(self, new_listname: str, save_current: bool = True):
        if save_current: self.save()
        self.__listname = new_listname
        self.reload()

    def append(self, elem: str): self.__content.append(elem)
    def delete(self, index: int): self.__content.pop(index)
    def clear(self): self.__content.clear()

    def save(self): save(self.__listname, self.__content)
    def reload(self): self.__content = load(self.__listname)

    def __del__(self): self.save()
