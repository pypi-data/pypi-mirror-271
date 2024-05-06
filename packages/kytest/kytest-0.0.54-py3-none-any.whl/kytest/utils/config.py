import os
import yaml

from kytest.utils.log import logger

local_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(local_path)


class Config:
    def __init__(self):
        self.file_path = os.path.join(root_path, 'running', 'conf.yml')

    def __getitem__(self, key):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        try:
            return yaml_data['common'][key]
        except:
            raise KeyError(f'{key} not in {yaml_data["common"]}')

    # def get_common(self, key):
    #     return self.get('common', key)
    #
    # def get_api(self, key):
    #     return self.get('api', key)
    #
    # def get_app(self, key):
    #     return self.get('app', key)
    #
    # def get_web(self, key):
    #     return self.get('web', key)

    def __setitem__(self, key, value):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        if key in yaml_data['common']:
            yaml_data['common'][key] = value
        else:
            raise KeyError(f'{key} not in {yaml_data["common"]}')
        with open(self.file_path, 'w', encoding="utf-8") as f:
            yaml.dump(yaml_data, f)

    def __len__(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return len(yaml_data['common'])

    def __repr__(self):  # 用于终端显示，与本博文关系不大
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return str(yaml_data['common'])

    def reset(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        yaml_data['common'] = {'base_url': None, 'browser': None, 'cookies': None, 'full': False, 'headers': None,
                               'headless': False, 'project': None, 'size': None, 'state': None, 'ocr_service': None}
        with open(self.file_path, 'w', encoding="utf-8") as f:
            yaml.dump(yaml_data, f)

    # def set_dict(self, module, data):
    #     with open(self.file_path, "r", encoding="utf-8") as f:
    #         yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
    #     yaml_data[module] = data
    #     with open(self.file_path, 'w', encoding="utf-8") as f:
    #         yaml.dump(yaml_data, f)
    #
    # def set_common(self, key, value):
    #     self.set('common', key, value)
    #
    # def set_common_dict(self, data):
    #     self.set_dict('common', data)
    #
    # def set_app(self, key, value):
    #     self.set('app', key, value)
    #
    # def set_app_dict(self, data):
    #     self.set_dict('app', data)
    #
    # def set_web(self, key, value):
    #     self.set('web', key, value)
    #
    # def set_web_dict(self, data):
    #     self.set_dict('web', data)


kconfig = Config()

if __name__ == '__main__':
    print(kconfig['project'])

