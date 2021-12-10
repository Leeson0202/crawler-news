
# title：标题  channelName：标签  content：文章内容 href：文章连接
class New:
    def __init__(self, title=None, channelName=None, content=None, href=None):
        self.title = ''
        self.content = ''
        self.length=0
        self.channelName=''
        self.href=''
        if title is not None and content is not None:
            self.title = title
            self.channelName=channelName
            self.content = content
            self.length=len(content)
            self.href = href
