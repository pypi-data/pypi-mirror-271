from cloudpy_org import processing_tools
import os
import json
this_dict = {}
#___________________________________________________
k = 'select'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<select id="@id" class="sensation inx" onchange="temp_input(this,'@k','');">
@options
</select>
<br>
""".replace('@k',k)
this_dict[k]['object'] = "<option>@object</option>"
this_dict[k]['params'] = ['@label_title','@options']
#___________________________________________________
k = 'radio_2_horizontal'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<div>
<a>&nbsp;&nbsp;
<span style="padding-right:10px;">
<input type="radio" name="radio_@id" id="@id_1" onchecked="temp_input(this,'@k','@option_1');>
<label for="@id_1" class ="sensation">@option_1</label>
</span>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<span>
<input type="radio" name="radio_@id" id="@id_2" onchecked="temp_input(this,'@k','@option_2');">
<label for="@id_2" class ="sensation">@option_2</label>
</span>
</a>
</div>
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@label_title','@option_1','@option_2']
#___________________________________________________
k = 'text_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<input id="@id" class="sensation" type="text" value="@text_content" style="border-bottom-width:1px;" onblur="temp_input(this,'@k','');">
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@label_title']
#___________________________________________________
k = 'pwd_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<input id="@id" class="sensation" type="pwd" value="@text_content" style="border-bottom-width:1px;" onblur="temp_input(this,'@k','');">
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@label_title']
#___________________________________________________
k = 'text_area'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<textarea id="@id" class="sensation inx" rows="@rowsnum" onblur="temp_input(this,'@k','');">@text_content</textarea>
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@label_title','@rowsnum']
#*******************************sections
this_sections = {}
k = 'right_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div id="@section_id" class="col-lg-@n" style="padding-right:10px;border-right:solid 1px orange;">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">@section_title</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']
#___________________________________________________
k = 'left_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div id="@section_id" class="col-lg-@n" style="padding-right:10px;border-left:solid 1px orange;">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">@section_title</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']

#___________________________________________________
k = 'no_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div id="@section_id" class="col-lg-@n" style="padding-right:10px;border:none;">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">@section_title</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']
main_dict = {}
main_dict['sections'] = this_sections
main_dict['inputs'] = this_dict
class cloudpy_org_web_client:
    def __init__(self, **kwargs):
        self.main_dict = main_dict
        self.pt = processing_tools()
        self.current_path = os.getcwd() + '/'
        #with open (self.current_path + 'dynamic_html.json', 'r') as f:
        #    self.main_dict = json.loads(f.read())
    def create_section(self,section_title:str,section_type:str='right_border',size:int=2):
        a = self.pt.camel_to_snake(section_title).replace('?','').replace('.','_').replace(',','')
        section_id = a[0:6] + a[::-1][0:6][::-1]
        rslt = self.main_dict['sections'][section_type]['html']\
        .replace('@section_id',section_id)\
        .replace('@section_title',section_title)\
        .replace('@n',str(size))
        return rslt.replace('\n','')
    def create_input(self,input_type:str,label_title:str,options:list=[],text_content:str='',rowsnum:int=3):
        a = self.pt.camel_to_snake(label_title)[0:12].replace('?','').replace('.','_').replace(',','')
        this_id = a[0:6] + a[::-1][0:6][::-1]
        rslt = self.main_dict['inputs'][input_type]['html']\
        .replace('@id',this_id)\
        .replace('@label_title',label_title)
        if input_type == 'select':
            opti = ''
            obj = self.main_dict['inputs'][input_type]['object']
            for this_option in options:
                opti += obj.replace('@object',this_option)
            rslt = rslt.replace('@options',opti)
        elif input_type == 'radio_2_horizontal':
            rslt = rslt\
            .replace('@option_1',options[0])\
            .replace('@option_2',options[1])
        elif input_type in['text_input','pwd_input','text_area']:
            rslt = rslt.replace('@text_content',text_content)
            if input_type == 'text_area':
                rslt = rslt.replace('@rowsnum',str(rowsnum))
        return rslt.replace('\n','')
    def complete_dynamic_form(self,dynamic_form:dict):
        sections = ''
        section_nums = list(dynamic_form['sections'].keys())
        section_nums.sort()
        for i in section_nums:
            ts = dynamic_form['sections'][i]
            inputs = ts['inputs']
            section = self.create_section(section_title=ts['section_title'],section_type=ts['section_type'],size=ts['size'])
            content = ""
            for j in inputs:
                if j['input_type'] in['text_input','pwd_input','text_area']:
                    text_content = ''
                    if 'text_content' in set(j.keys()):
                        text_content=j['text_content']
                    if j['input_type'] == 'text_area':
                        rowsnum = j['rowsnum']
                        content += self.create_input(input_type=j['input_type'],label_title=j['label_title'],text_content=text_content,rowsnum=rowsnum)
                    else:
                        content += self.create_input(input_type=j['input_type'],label_title=j['label_title'],text_content=text_content)
                else:
                    options = []
                    if 'options' in set(j.keys()):
                        options=j['options']
                    content += self.create_input(input_type=j['input_type'],label_title=j['label_title'],options=options)
            sections += section.replace('@content',content) 
        complete_form = '<div class="row" style="width:1600px;position:relative;left:50px;top:-10px;">@sections</div>'
        complete_form =complete_form.replace('@sections',sections)
        return complete_form