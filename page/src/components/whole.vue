<template>
    <div>
        <div v-pre data="{{qwvalue}}"></div>      
        <el-drawer
            title="推荐文章"
            direction="ltr"
            :visible.sync="drawer"
            :with-header="true"
            size="50%">
            <div class="recoroll">
                <div>
                    关键词 {{rw}}
                </div>
                <ul
                class="recolist"
                v-infinite-scroll="load"
                infinite-scroll-disabled="disabled">
                    <li 
                    v-for="(pp,i) in passages" 
                    :key="i" 
                    class="recolist-item">
                        <!-- <el-link 
                        :href="url" 
                        target="_blank">
                        {{pp}}
                        </el-link> -->
                        <el-button 
                        type="text" 
                        @click="go(pp.id)"
                        >{{pp.title}}</el-button>
                    </li>
                </ul>
            </div>
        </el-drawer>
        <el-container>
            <el-header>
                <el-row>
                    <el-col :span="24">
                        <div class="grid-content title_clr">
                            <el-button 
                            type="text" 
                            v-on:click="Search"
                            >
                            Home
                            </el-button>
                            <el-button 
                            type="text"
                            @click="drawer = true" 
                            >
                            Recommend
                            </el-button>
                            <!-- <el-input 
                                class="searchinput" 
                                v-model="input" 
                                placeholder="搜索内容">
                                    <el-button 
                                    slot="prepend" 
                                    @click="drawer = true" 
                                    icon="el-icon-collection-tag">
                                    </el-button>
                            </el-input> -->
                        </div>
                    </el-col>
                </el-row>
            </el-header>
            <el-main>
                <div class="roll">
                    <!-- <div
                    class="list-item">
                        <div
                        style="height:50px;"
                        ></div>
                        <p class="ptitle">{{qwtitle}}</p>
                        <div
                        class="ptext"
                        v-for="(line,id) in qwvalue" 
                        :key=id
                        >
                        {{line}}
                        </div>
                        <div
                        style="height:100px;"
                        ></div>
                        <el-divider class="divider">
                        </el-divider>
                    </div> -->
                    <div
                    v-for="(paragragh,id) in qw" 
                    :key="id" 
                    class="list-item">
                        <div
                        style="height:50px;"
                        ></div>
                        <p class="ptitle">{{paragragh.title}}</p>
                        <div
                        class="ptext"
                        v-for="(line,id) in paragragh.value" 
                        :key=id
                        >
                        {{line}}
                        </div>
                        <!-- <div
                        class="ptext"
                        >
                        {{paragragh.value}}
                        </div> -->
                        <div
                        style="height:100px;"
                        ></div>
                        <el-divider class="divider">
                        </el-divider>
                    </div>
                </div>
            </el-main>
        </el-container>

    </div>  
</template>

<script>

export default {
    data() {
        return {
            rw:'a',
            options: [],
            sinvalue: '',
            mutvalue: '',
            date1:'',
            drawer: false,
            input: "",
            ph:"搜索内容",
            count: 10,
            loading: false,
            qwvalue:'',
            qwtitle:'',
            qw:[

// {title:'文首',value:'山东省青岛市黄岛区人民法院\n民事判决书\n（2016）鲁0211民初12571号\n'},
// {title:'当事人',value:'原告：青岛天一集团红旗电机有限公司，住所地青岛市黄岛区世纪大道1588号。\n法定代表人：孙国华，董事长。\n委托诉讼代理人：朱业华，山东汇正律师事务所律师。\n被告：青岛市黄岛区第一中学，住所地青岛市黄岛区广州路北段。\n法定代表人：管仁福，校长。\n委托诉讼代理人：宋成宝，山东雅圣律师事务所律师。'},
// {title:'诉讼记录',value:'\n原告青岛天一集团红旗电机有限公司（以下简称“天一公司”）与被告青岛市黄岛区第一中学（以下简称“黄岛一中”）保证合同纠纷一案，本案于2016年8月11日立案后，依法适用简易程序公开开庭进行了审理。原告天一公司的委托诉讼代理人朱业华及被告黄岛一中的委托诉讼代理人宋成宝到庭参加诉讼。本案现已审理终结。'},
// {title:'案件基本情况',value:'\n天一公司向本院提出诉讼请求：1、黄岛一中支付资金占用利息1058186.58元；2、黄岛一中支付天一公司为其垫付的银行贷款逾期利息25205.65元；3、黄岛一中承担本案诉讼费用。事实和理由：2006年年底，在政府有关部门的协调下，天一公司为黄岛一中在中国工商银行股份有限公司胶南支行的600万元贷款提供担保。2008年1月至2月期间，因上述贷款到期后黄岛一中未按时偿还，中国工商银行股份有限公司胶南支行即按合同约定分五次从天一公司扣款5941170.51元（借款本金5915964.86元、逾期利息25205.65元），用于偿还黄岛一中的上述借款本息。2008年至2011年期间，黄岛一中通过财政本门分四次偿还天一公司上述借款本金5915964.86元，但尚有双方约定的资金占用利息1058186.58元及天一公司为其垫付的银行贷款逾期利息25205.65元未予偿还。\n黄岛一中辩称，天一公司为黄岛一中提供担保属实，但对天一公司主张的资金占用利息不认可，双方对此未作任何约定，属天一公司单方意见；即便属实，天一公司的该项主张已经超过两年诉讼时效。\n本案当事人围绕诉讼请求依法提交了证据，本院组织当事人进行了证据质证。对当事人无异议的证据，本院予以确认并在卷佐证。\n对当事人无争议的事实，本院确认如下：2006年年底，天一公司为黄岛一中在中国工商银行股份有限公司胶南支行的600万元贷款提供担保。2008年1月至2月期间，因上述贷款到期后黄岛一中未按时偿还，中国工商银行股份有限公司胶南支行即按合同约定分五次从天一公司扣款5941170.51元（借款本金5915964.86元、逾期利息25205.65元），用于偿还黄岛一中的上述借款本息。2008年至2011年期间，黄岛一中通过财政本门分四次归还天一公司上述借款本金5915964.86元。2016年4月12日，天一公司向黄岛区财政局出具《关于胶南一中担保利息的申请》，载明了上述事实，还载明尚有资金占用利息1058186.58元及逾期利息25205.65元合计1083392.23元未归还，黄岛一中在“情况属实”处加盖公章。\n双方对天一公司起诉是否已过诉讼时效以及欠款的数额有争议。黄岛一中主张，天一公司主张的利息发生在2011年7月13日前，其应在2013年7月13日前向黄岛一中主张权利，因此天一公司起诉已经超过两年诉讼时效；双方约定的不变的年利率为6.732％，天一公司将上述利率上浮30％，不符合借款合同及担保合同的约定；天一公司提交的申请书系其作为一方当事人向另一方当事人黄岛区财政局作出的约定，而非天一公司与黄岛一中的约定，该申请系黄岛一中协助天一公司向财政部门申请资金占用利息而出具的，不能将黄岛一中的协助行为理解为义务。\n天一公司主张，借款合同及担保合同签订后，天一公司履行了担保义务，替黄岛一中偿还了银行借款本息，期间存在占用资金的利息，该利息天一公司同意按照年利率6％计算，共计790884.98元；双方对资金占用利息未约定支付时间，应适用20年的诉讼时效。\n黄岛一中认可按照年利率6％计算资金占用利息，但认为不应支付该款项。\n'},
// {title:'裁判分析过程',value:'本院认为，关于资金占用期间的利息应否支付问题，双方均认可黄岛一中存在逾期支付贷款问题，且在天一公司提交的申请书中黄岛一中亦认可资金占用利息，故该款项黄岛一中应当支付；关于数额问题，双方对按年利率6％标准计算无异议，按照该标准计算的利息为790884.98元，再加上双方无异议的逾期25205.65元，共计816090.63元，黄岛一中应当支付。关于诉讼时效问题，双方对资金占用利息以及逾期利息未约定支付时间，故应适用20年的诉讼时效，天一公司起诉未超过诉讼时效。根据《中华人民共和国担保法》第十二条、第二十一条、第三十一条，《中华人民共和国民事诉讼法》第六十四条第一款之规定，判决如下：'},
// {title:'判决结果',value:'\n一、青岛市黄岛区第一中学于本判决生效之日起十日内给付青岛天一集团红旗电机有限公司资金占用利息790884.98元；\n二、青岛市黄岛区第一中学于本判决生效之日起十日内给付青岛天一集团红旗电机有限公司逾期利息25205.65元；\n三、驳回青岛天一集团红旗电机有限公司的其他诉讼请求。\n如果被告未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条规定，加倍支付迟延履行期间的债务利息。\n本案案件受理费14551元，减半收取7275.50元，由青岛天一集团红旗电机有限公司负担1295元，由青岛市黄岛区第一中学负担5980.50元。\n如不服本判决，可在判决书送达之日起十五日内向本院递交上诉状，并按对方当事人的人数提出副本，上诉于山东省青岛市中级人民法院。'},
// {title:'文尾',value:'\n审判员张成镇\n二〇一七年三月十三日\n书记员丁钰杰\n'},

            ],
            passages:[
                {title:'名字',id:1003}
            ]
        }
    },
    computed: {
        noMore () {
            return this.count >= 100
        },
        disabled () {
            return this.loading || this.noMore
        }
    },
    // beforeMount(){
    //     var value = document.getElementsByTagName('div')[1].getAttribute('data') || '';
    //     // var title='QW'
    //     // console.log(title)
    //     console.log(value)
    //     // this.qw=[{title:title,value:value}]
    // },
    mounted:function(){
        // this.qw=[{title:title,value:value}]
        // var pre = window.location.href
        // pre = pre.split('/')
        // console.log(pre)
        // // var id = pre[pre.length()-1]
        

        this.passages=[]
        var url='get/'
        console.log('jump to search' )
        var req = new XMLHttpRequest();
        req.open('GET', url, true);
        req.setRequestHeader("Content-type","application/json");
        req.send()
        var vue = this
        req.onreadystatechange = function () {
            console.log('response')
            if (req.readyState == 4 && req.status == 200) {
                var json = req.responseText;
                json = JSON.parse(json)
                console.log(json)
                if (json['n']==1){
                    var y= [
                        '文首',
                        '当事人',
                        '诉讼记录',
                        '案件基本情况',
                        '判决结果',
                        '文尾',            
                    ]
                    for (var el of y){
                        var temp = json[el]
                        temp=temp.split(' ')
                        console.log(el)
                        console.log(temp)
                        vue.qw.push({title:el,value:temp})
                        console.log(vue.qw)
                    }
                }else{
                    var title = json['title']
                    var answer = json['value']
                    answer = answer.split(' ')
                    vue.qw.push({title:title,value:answer})
                    vue.qwtitle=title
                    vue.qwvalue=answer
                }
            }
        };

        var reco='reco/'
        console.log('reco' )
        var rreq = new XMLHttpRequest();
        rreq.open('GET', reco, true);
        rreq.setRequestHeader("Content-type","application/json");
        rreq.send()
        rreq.onreadystatechange = function () {
            console.log('response')
            if (rreq.readyState == 4 && rreq.status == 200) {
                var rjson = rreq.responseText;
                rjson = JSON.parse(rjson)
                console.log(rjson)
                var rpa=rjson['passage']
                for (var i in rpa){
                    vue.passages.push(rpa[i])
                }
                vue.rw=rjson['rw']
            }
        };
    },
    methods:{
        go(xmlid){
            var pre = window.location.host
            console.log(pre)
            var url ='//' + pre +'/p/'+xmlid.toString()
            window.open(url)
        },
        Search:function () {
            this.loading=false
            this.passages=[]
            // var url='back/'
            var pre = window.location.host
            console.log(pre)
            console.log('jump to search' )
            window.open('//'+pre);
            // var req = new XMLHttpRequest();
            // req.open('GET', url, true);
            // req.setRequestHeader("Content-type","application/json");
            // req.send()
            // // var vue = this
            // req.onreadystatechange = function () {
            //     console.log('response')
            //     if (req.readyState == 4 && req.status == 200) {
            //         // var html = req.responseText;
            //         // var newWindow = window.open();
            //         // newWindow.document.write(html);
            //     }
            // };
        }
    }
}
</script>

<style scoped>
    .el-header{
        height: 60px;
        padding:0;
    }
    .el-main{
        padding: 0;

    }
    .el-container{
        height: 100vh;
    }
    .el-row {
        height: 100%;
        
    }
    .el-col {
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    .title_clr {
        background: #1d5cb4;
    }
    .grid-content {

        height: 100%;
        /* padding-top:10px; */
    }
    .searchinput{
        margin-top:10px;
        margin-bottom:10px;

        height: 40px;
        width:95%;
    }
    .roll{
        height: 100%;
        overflow: auto;
    }
    .list{
        height: 100%;
        margin: 0;
        padding: 0;
        overflow:auto;

    }
    .list-item{
        /* min-height: 200px; */
        display:block; 
        overflow: hidden;
        position: relative;
        /* text-overflow: ellipsis; */
        /* white-space: nowrap; */
        list-style: none;

		text-align: left;
		text-indent: 2em;
    }
    .divider{
        position: absolute;
        bottom: 0px;
        margin-left:5%;
        margin-right:5%;
        width: 90%;

    }
    .ptitle{
        font-family: "微软雅黑";
        font-size:25px;
		font-weight: bold;
		line-height: 30px;
        /* display: table-cell;
		vertical-align: middle; */
        margin: 10px 15% 50px 15%;
        width: 70%;

    }
    .ptext{
        font-family: "lucida grande", "lucida sans unicode", lucida, helvetica, "Hiragino Sans GB", "MicrosoftYaHei", "WenQuanYi Micro Hei", sans-serif;
        font-size:20px;
		/* font-weight: bold; */
		line-height: 24px;
        /* display: table-cell; */
		/* vertical-align: middle; */
        margin: 0 auto;
        width: 70%;
    }
    .recoroll{
        height: 100%;
        overflow: auto;

    }
    .recolist{
        height: 100%;
        width: 80%;
        margin: 0 auto;
        padding: 0;
        overflow:auto;

    }
    .recolist-item{
        height: 10%;
        width: 70%;
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        list-style: none;
        margin: 0 15% 0 15%;
    }
</style>