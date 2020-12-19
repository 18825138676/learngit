from werkzeug.routing import  BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self,url_map,*args):
        super(RegexConverter,self).__init__(url_map)
        #将接受的第1个参数当作匹配规则进行保存
        self.regex=args[0]

    def to_url(self, value):
        '''

        使用url_for反向生成URL时，传递的参数，返回的值用于生成URL中的参数

        :param value:
        :return:
        '''
        val=super(RegexConverter,self).to_url(value)
        return val

class MobileConverter(BaseConverter):
    def __init__(self,url_map):
        super().__init__(url_map)
        self.regex=r'1[3456789]\d{9}'
