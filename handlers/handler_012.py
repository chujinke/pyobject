# encoding=utf-8
from handlers.public import Request
from tornado import gen

class  GetHandler(Request):
    """该Handler完成编号12,16,17,18,19协议
       |/douban/tag/%E8%8B%B1%E5%9B%BD%20%E5%96%9C%E5%89%A7%202015|get|12|html|No.143 验证参数{'start':'20','type':'S'}|
       16，17，18，19协议按照path返回不同页面
    """

    @gen.coroutine
    def get(self,tag_name):
        """处理GET请求"""

        tmpl = '''<script id="suggResult" type="text/x-jquery-tmpl">
  <li data-link="{{= url}}">
            <a href="{{= url}}" onclick="moreurl(this, {from:'movie_search_sugg', query:'{{= keyword }}', subject_id:'{{= id}}', i: '{{= index}}', type: '{{= type}}'})">
            <img src="{{= img}}" width="40" />
            <p>
                <em>{{= title}}</em>
                {{if year}}
                    <span>{{= year}}</span>
                {{/if}}
                {{if sub_title}}
                    <br /><span>{{= sub_title}}</span>
                {{/if}}
                {{if address}}
                    <br /><span>{{= address}}</span>
                {{/if}}
                {{if episode}}
                    {{if episode=="unknow"}}
                        <br /><span>集数未知</span>
                    {{else}}
                        <br /><span>共{{= episode}}集</span>
                    {{/if}}
                {{/if}}
            </p>
        </a>
        </li>
  </script>



'''
        verification_tag =  u"英国 喜剧 2015"
        #判断tag_name是否为"英国 喜剧 2015",如果是检查该链接参数
        if tag_name ==verification_tag:
            if Request.verification_query(self):
                tag_name = tag_name+".htm"
                self.render(tag_name,tmpl = tmpl)
            else:
                self.set_status(status_code=404)
        else:
            tag_name = tag_name+".htm"
            self.render(tag_name,tmpl = tmpl)



